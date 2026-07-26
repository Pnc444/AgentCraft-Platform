import { API_BASE, apiClient, tryRefreshAccessToken } from "@/lib/api/client";
import { useAuthStore } from "@/stores/authStore";

export interface TutorSuggestions {
  suggestions: string[];
  available: boolean;
}

export interface TutorTurn {
  role: "user" | "assistant";
  text: string;
}

export function getTutorSuggestions(courseSlug: string, lessonSlug: string) {
  const query = new URLSearchParams({
    course_slug: courseSlug,
    lesson_slug: lessonSlug,
  });
  return apiClient<TutorSuggestions>(`/tutor/suggestions/?${query}`);
}

interface StreamArgs {
  message: string;
  courseSlug: string;
  lessonSlug: string;
  history: TutorTurn[];
  signal: AbortSignal;
  onToken: (text: string) => void;
}

/**
 * POST a question and stream the answer back as SSE.
 *
 * Uses fetch rather than EventSource because EventSource cannot send an
 * Authorization header, and the tutor endpoint is authenticated.
 */
export async function streamTutorAnswer({
  message,
  courseSlug,
  lessonSlug,
  history,
  signal,
  onToken,
}: StreamArgs): Promise<void> {
  const send = async (token: string | null) =>
    fetch(`${API_BASE}/tutor/ask/`, {
      method: "POST",
      signal,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({
        message,
        course_slug: courseSlug,
        lesson_slug: lessonSlug,
        history,
      }),
    });

  let response = await send(useAuthStore.getState().accessToken);

  if (response.status === 401) {
    const refreshed = await tryRefreshAccessToken();
    if (!refreshed) throw new Error("Your session expired. Sign in again.");
    response = await send(refreshed);
  }

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const errors = body?.errors;
    const detail = Array.isArray(errors) ? errors[0] : errors;
    throw new Error(
      typeof detail === "string" ? detail : "The tutor could not be reached."
    );
  }
  if (!response.body) throw new Error("The tutor returned an empty response.");

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let streamError: string | null = null;

  // SSE frames are separated by a blank line. Hold partial frames in `buffer`.
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    let split = buffer.indexOf("\n\n");
    while (split !== -1) {
      const frame = buffer.slice(0, split);
      buffer = buffer.slice(split + 2);
      split = buffer.indexOf("\n\n");

      let event = "message";
      const dataLines: string[] = [];
      for (const line of frame.split("\n")) {
        if (line.startsWith("event:")) event = line.slice(6).trim();
        else if (line.startsWith("data:")) dataLines.push(line.slice(5).trim());
      }
      if (!dataLines.length) continue;

      let payload: { text?: string; message?: string };
      try {
        payload = JSON.parse(dataLines.join("\n"));
      } catch {
        continue;
      }

      if (event === "token" && payload.text) onToken(payload.text);
      else if (event === "error") streamError = payload.message ?? "Tutor error.";
    }
  }

  if (streamError) throw new Error(streamError);
}
