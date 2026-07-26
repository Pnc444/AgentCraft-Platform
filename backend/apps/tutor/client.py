"""Minimal streaming OpenRouter client.

Stdlib only — no new dependency, and urllib streams the SSE body fine.

Two things this handles that a naive client does not:

1. **Free models rate-limit constantly.** A single hardcoded model produces a
   tutor that is broken half the time, which is the failure mode we are fixing.
   `stream_chat` walks a fallback chain and only surfaces an error once every
   model has refused.

2. **Reasoning models leak chain-of-thought into `content`.** The strongest free
   model (nemotron-3-ultra) will happily emit "The user asks... so we should
   respond" to a beginner. We send `reasoning: {"exclude": True}` and also strip
   any `<think>` block that slips through.
"""

from __future__ import annotations

import json
import logging
import re
import urllib.error
import urllib.request
from collections.abc import Iterator

from django.conf import settings

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Some models emit a visible reasoning preamble despite reasoning.exclude.
_THINK_BLOCK = re.compile(r"<think>.*?</think>\s*", re.DOTALL | re.IGNORECASE)
_OPEN_THINK = re.compile(r"<think>", re.IGNORECASE)


class TutorUnavailable(RuntimeError):
    """Every model in the chain refused. Carries a learner-safe message."""

    def __init__(self, message: str, *, detail: str = ""):
        super().__init__(message)
        self.learner_message = message
        self.detail = detail


def _configured_models() -> list[str]:
    models = [m.strip() for m in settings.OPENROUTER_TUTOR_MODELS if m and m.strip()]
    if not models:
        raise TutorUnavailable("The tutor has no model configured.")
    return models


def _request(model: str, messages: list[dict], max_tokens: int, temperature: float):
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": True,
        # Keep the model's scratchpad out of the learner's face.
        "reasoning": {"exclude": True},
    }
    request = urllib.request.Request(
        OPENROUTER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            # OpenRouter attribution headers — good citizenship, not required.
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": "AgentCraft",
        },
        method="POST",
    )
    return urllib.request.urlopen(request, timeout=settings.OPENROUTER_TIMEOUT_SECONDS)


def _iter_sse_text(response) -> Iterator[str]:
    """Yield content deltas from an OpenRouter SSE stream."""
    for raw in response:
        line = raw.decode("utf-8", errors="replace").strip()
        # Keepalive comments arrive as ": OPENROUTER PROCESSING".
        if not line or line.startswith(":"):
            continue
        if not line.startswith("data:"):
            continue
        data = line[len("data:") :].strip()
        if data == "[DONE]":
            return
        try:
            chunk = json.loads(data)
        except json.JSONDecodeError:
            continue
        if chunk.get("error"):
            raise TutorUnavailable(
                "The tutor hit an error mid-answer.",
                detail=str(chunk["error"])[:300],
            )
        for choice in chunk.get("choices") or []:
            piece = (choice.get("delta") or {}).get("content")
            if piece:
                yield piece


class _ThinkStripper:
    """Drops <think>…</think> preambles from a token stream.

    Buffers only while a block is open, so normal output stays fully streaming.
    """

    def __init__(self) -> None:
        self._buffer = ""
        self._in_think = False

    def push(self, piece: str) -> str:
        self._buffer += piece
        out = ""
        while self._buffer:
            if self._in_think:
                end = self._buffer.lower().find("</think>")
                if end == -1:
                    return out
                self._buffer = self._buffer[end + len("</think>") :].lstrip()
                self._in_think = False
                continue
            match = _OPEN_THINK.search(self._buffer)
            if not match:
                # Hold back a possible partial "<think" straddling two chunks.
                safe = self._buffer[: max(0, len(self._buffer) - 7)]
                if "<" in self._buffer[len(safe) :]:
                    out += safe
                    self._buffer = self._buffer[len(safe) :]
                else:
                    out += self._buffer
                    self._buffer = ""
                return out
            out += self._buffer[: match.start()]
            self._buffer = self._buffer[match.end() :]
            self._in_think = True
        return out

    def flush(self) -> str:
        if self._in_think:
            return ""
        rest, self._buffer = self._buffer, ""
        return _THINK_BLOCK.sub("", rest)


def stream_chat(
    messages: list[dict],
    *,
    max_tokens: int | None = None,
    temperature: float = 0.3,
) -> Iterator[tuple[str, str]]:
    """Stream a completion, walking the model fallback chain.

    Yields ``(event, value)`` where event is:
      ``model``  — the model that answered (emitted once, before any text)
      ``text``   — a content delta
    Raises :class:`TutorUnavailable` if every model refuses.
    """
    if not settings.OPENROUTER_API_KEY:
        raise TutorUnavailable(
            "The tutor is not configured on this server yet.",
            detail="OPENROUTER_API_KEY is empty",
        )

    max_tokens = max_tokens or settings.OPENROUTER_MAX_TOKENS
    failures: list[str] = []

    for model in _configured_models():
        try:
            response = _request(model, messages, max_tokens, temperature)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:300]
            failures.append(f"{model}: HTTP {exc.code}")
            logger.warning("tutor model %s failed: HTTP %s %s", model, exc.code, body)
            continue
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            failures.append(f"{model}: {type(exc).__name__}")
            logger.warning("tutor model %s unreachable: %s", model, exc)
            continue

        stripper = _ThinkStripper()
        produced_text = False
        try:
            with response:
                yield ("model", model)
                for piece in _iter_sse_text(response):
                    cleaned = stripper.push(piece)
                    if cleaned:
                        produced_text = True
                        yield ("text", cleaned)
                tail = stripper.flush()
                if tail:
                    produced_text = True
                    yield ("text", tail)
        except TutorUnavailable:
            # Mid-stream error. If the learner already saw text we cannot
            # silently switch models, so surface it.
            if produced_text:
                raise
            failures.append(f"{model}: stream error")
            continue
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if produced_text:
                raise TutorUnavailable(
                    "The tutor's connection dropped mid-answer.",
                    detail=f"{model}: {type(exc).__name__}",
                ) from exc
            failures.append(f"{model}: {type(exc).__name__}")
            continue

        if produced_text:
            return
        failures.append(f"{model}: empty response")

    raise TutorUnavailable(
        "Every tutor model is busy right now. Free models rate-limit — try again in a moment.",
        detail="; ".join(failures),
    )
