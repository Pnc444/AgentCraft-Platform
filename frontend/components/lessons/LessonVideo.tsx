"use client";

import { useEffect, useId, useMemo, useRef, useState } from "react";

interface LessonVideoProps {
  url: string;
  title?: string;
  onWatched?: (details: VideoCompletionDetails) => void;
  watched?: boolean;
  requireFullWatch?: boolean;
}

export interface VideoCompletionDetails {
  source: "youtube" | "direct" | "manual";
  durationSeconds: number;
  watchedSeconds: number;
}

const VIDEO_SEEK_TOLERANCE_SECONDS = 2;
const VIDEO_REWIND_PADDING_SECONDS = 0.25;
const VIDEO_COMPLETION_BUFFER_SECONDS = 3;
const VIDEO_COMPLETION_MIN_RATIO = 0.95;

export function videoCompletionThresholdSeconds(durationSeconds: number): number {
  if (!Number.isFinite(durationSeconds) || durationSeconds <= 0) return Number.POSITIVE_INFINITY;
  return Math.max(durationSeconds - VIDEO_COMPLETION_BUFFER_SECONDS, durationSeconds * VIDEO_COMPLETION_MIN_RATIO);
}

export function hasMetRequiredWatchTime(
  watchedSeconds: number,
  durationSeconds: number
): boolean {
  if (!Number.isFinite(watchedSeconds) || watchedSeconds < 0) return false;
  return watchedSeconds >= videoCompletionThresholdSeconds(durationSeconds);
}

export function isForwardSeekBeyondAllowed(
  watchedSeconds: number,
  currentSeconds: number
): boolean {
  if (!Number.isFinite(currentSeconds) || currentSeconds < 0) return false;
  return currentSeconds > watchedSeconds + VIDEO_SEEK_TOLERANCE_SECONDS;
}

export function resumePlaybackSeconds(watchedSeconds: number): number {
  if (!Number.isFinite(watchedSeconds) || watchedSeconds <= 0) return 0;
  return Math.max(0, watchedSeconds - VIDEO_REWIND_PADDING_SECONDS);
}

/** Extract a YouTube video id from watch, youtu.be, shorts, or embed URLs. */
export function youtubeVideoId(url: string): string | null {
  try {
    const parsed = new URL(url.trim());
    const host = parsed.hostname.replace(/^www\./, "");

    if (host === "youtu.be") {
      const id = parsed.pathname.split("/").filter(Boolean)[0];
      return id || null;
    }

    if (host === "youtube.com" || host === "m.youtube.com" || host === "youtube-nocookie.com") {
      const v = parsed.searchParams.get("v");
      if (v) return v;

      const parts = parsed.pathname.split("/").filter(Boolean);
      if (parts[0] === "embed" || parts[0] === "shorts" || parts[0] === "live") {
        return parts[1] || null;
      }
    }
  } catch {
    return null;
  }
  return null;
}

/** True for locally-hosted or direct video files (e.g. /videos/lessons/foo.mp4). */
export function isDirectVideoUrl(url: string): boolean {
  const clean = url.trim().split(/[?#]/)[0].toLowerCase();
  return /\.(mp4|webm|mov|m4v)$/.test(clean);
}

declare global {
  interface Window {
    YT?: {
      Player: new (
        el: string | HTMLElement,
        opts: {
          videoId: string;
          width?: string | number;
          height?: string | number;
          playerVars?: Record<string, string | number>;
          events?: {
            onStateChange?: (e: { data: number }) => void;
          };
        }
      ) => {
        destroy?: () => void;
        getCurrentTime?: () => number;
        getDuration?: () => number;
        playVideo?: () => void;
        seekTo?: (seconds: number, allowSeekAhead?: boolean) => void;
      };
      PlayerState?: { ENDED: number; PLAYING: number };
    };
    onYouTubeIframeAPIReady?: () => void;
  }
}

function loadYouTubeApi(): Promise<void> {
  if (typeof window === "undefined") return Promise.resolve();
  if (window.YT?.Player) return Promise.resolve();
  return new Promise((resolve) => {
    const prior = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => {
      prior?.();
      resolve();
    };
    if (!document.getElementById("youtube-iframe-api")) {
      const tag = document.createElement("script");
      tag.id = "youtube-iframe-api";
      tag.src = "https://www.youtube.com/iframe_api";
      document.body.appendChild(tag);
    }
  });
}

export function LessonVideo({
  url,
  title = "Lesson video",
  onWatched,
  watched = false,
  requireFullWatch = false,
}: LessonVideoProps) {
  const id = youtubeVideoId(url);
  const reactId = useId().replace(/:/g, "");
  const containerId = `yt-player-${reactId}`;
  const playerRef = useRef<{
    destroy?: () => void;
    getCurrentTime?: () => number;
    getDuration?: () => number;
    playVideo?: () => void;
    seekTo?: (seconds: number, allowSeekAhead?: boolean) => void;
  } | null>(null);
  const nativeVideoRef = useRef<HTMLVideoElement | null>(null);
  const watchedRef = useRef(watched);
  const enforceSequentialWatchRef = useRef(requireFullWatch && !watched);
  const maxWatchedSecondsRef = useRef(0);
  const durationSecondsRef = useRef(0);
  const completionReportedRef = useRef(watched);
  const warningTimeoutRef = useRef<number | null>(null);
  const [showCompletionOverlay, setShowCompletionOverlay] = useState(false);
  const [showSeekWarning, setShowSeekWarning] = useState(false);
  const enforceSequentialWatch = requireFullWatch && !watched;
  const completionMessage = useMemo(
    () =>
      watched
        ? "Video complete. The Recap Quiz is unlocked."
        : "Video complete. You can continue to the Recap Quiz.",
    [watched]
  );

  useEffect(() => {
    watchedRef.current = watched;
    completionReportedRef.current = watched;
  }, [watched]);

  useEffect(() => {
    enforceSequentialWatchRef.current = requireFullWatch && !watched;
  }, [requireFullWatch, watched]);

  useEffect(() => {
    return () => {
      if (warningTimeoutRef.current !== null) {
        window.clearTimeout(warningTimeoutRef.current);
      }
    };
  }, []);

  function flashSeekWarning() {
    setShowSeekWarning(true);
    if (warningTimeoutRef.current !== null) {
      window.clearTimeout(warningTimeoutRef.current);
    }
    warningTimeoutRef.current = window.setTimeout(() => {
      setShowSeekWarning(false);
      warningTimeoutRef.current = null;
    }, 2200);
  }

  function maybeRecordProgress(currentSeconds: number, durationSeconds: number) {
    if (Number.isFinite(durationSeconds) && durationSeconds > 0) {
      durationSecondsRef.current = durationSeconds;
    }

    if (!Number.isFinite(currentSeconds) || currentSeconds < 0) {
      return false;
    }

    if (
      enforceSequentialWatchRef.current &&
      !completionReportedRef.current &&
      isForwardSeekBeyondAllowed(maxWatchedSecondsRef.current, currentSeconds)
    ) {
      return true;
    }

    maxWatchedSecondsRef.current = Math.max(maxWatchedSecondsRef.current, currentSeconds);
    return false;
  }

  function emitCompletion(source: VideoCompletionDetails["source"]) {
    const durationSeconds = durationSecondsRef.current;
    const watchedSeconds = maxWatchedSecondsRef.current;

    if (!hasMetRequiredWatchTime(watchedSeconds, durationSeconds)) {
      return false;
    }

    if (!completionReportedRef.current) {
      completionReportedRef.current = true;
      onWatched?.({
        source,
        durationSeconds,
        watchedSeconds,
      });
    }

    setShowCompletionOverlay(true);
    return true;
  }

  function blockYouTubeSeek(player: {
    seekTo?: (seconds: number, allowSeekAhead?: boolean) => void;
  } | null) {
    player?.seekTo?.(resumePlaybackSeconds(maxWatchedSecondsRef.current), true);
    flashSeekWarning();
  }

  function replayDirectVideo() {
    const video = nativeVideoRef.current;
    if (!video) return;
    setShowCompletionOverlay(false);
    video.currentTime = 0;
    void video.play().catch(() => {
      /* ignore autoplay rejection */
    });
  }

  function replayYouTubeVideo() {
    const player = playerRef.current;
    if (!player) return;
    setShowCompletionOverlay(false);
    player.seekTo?.(0, true);
    player.playVideo?.();
  }

  function renderCompletionOverlay(onReplay: () => void) {
    if (!showCompletionOverlay) return null;

    return (
      <div className="absolute inset-0 flex items-center justify-center bg-craft-navy/70 p-4 text-center">
        <div className="max-w-sm rounded-2xl border border-craft-border bg-craft-surface/95 px-5 py-4 shadow-elevated backdrop-blur-sm">
          <p className="text-base font-semibold text-craft-ink">{completionMessage}</p>
          <p className="mt-2 text-sm text-craft-muted">
            Review the video again if you want, or continue to the quiz.
          </p>
          <div className="mt-4 flex justify-center">
            <button type="button" onClick={onReplay} className="btn-secondary">
              Replay Video
            </button>
          </div>
        </div>
      </div>
    );
  }

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    let pollId: number | null = null;

    loadYouTubeApi().then(() => {
      if (cancelled || !window.YT?.Player) return;
      const ended = window.YT.PlayerState?.ENDED ?? 0;
      const playing = window.YT.PlayerState?.PLAYING ?? 1;
      playerRef.current = new window.YT.Player(containerId, {
        videoId: id,
        width: "100%",
        height: "100%",
        playerVars: {
          rel: 0,
          modestbranding: 1,
          playsinline: 1,
        },
        events: {
          onStateChange: (event) => {
            const player = playerRef.current;
            const currentSeconds = player?.getCurrentTime?.() ?? 0;
            const durationSeconds = player?.getDuration?.() ?? durationSecondsRef.current;

            if (maybeRecordProgress(currentSeconds, durationSeconds)) {
              blockYouTubeSeek(player);
              return;
            }

            if (event.data === playing && pollId === null) {
              pollId = window.setInterval(() => {
                const current = playerRef.current?.getCurrentTime?.() ?? 0;
                const duration = playerRef.current?.getDuration?.() ?? durationSecondsRef.current;
                if (maybeRecordProgress(current, duration)) {
                  blockYouTubeSeek(playerRef.current);
                }
              }, 500);
            }

            if (event.data !== playing && pollId !== null) {
              window.clearInterval(pollId);
              pollId = null;
            }

            if (event.data === ended) {
              if (emitCompletion("youtube")) {
                return;
              }

              if (enforceSequentialWatchRef.current) {
                blockYouTubeSeek(player);
              }
            }
          },
        },
      });
    });

    return () => {
      cancelled = true;
      if (pollId !== null) {
        window.clearInterval(pollId);
      }
      try {
        playerRef.current?.destroy?.();
      } catch {
        /* ignore */
      }
      playerRef.current = null;
    };
  }, [containerId, id, onWatched]);

  if (isDirectVideoUrl(url)) {
    return (
      <div className="space-y-2">
        <div className="relative overflow-hidden rounded-xl border border-craft-border bg-black shadow-elevated ring-1 ring-black/20">
          {/* eslint-disable-next-line jsx-a11y/media-has-caption */}
          <video
            ref={nativeVideoRef}
            className="aspect-video w-full"
            src={url}
            controls
            playsInline
            preload="metadata"
            title={title}
            onLoadedMetadata={(event) => {
              durationSecondsRef.current = event.currentTarget.duration;
            }}
            onSeeking={(event) => {
              const video = event.currentTarget;
              if (maybeRecordProgress(video.currentTime, video.duration)) {
                video.currentTime = resumePlaybackSeconds(maxWatchedSecondsRef.current);
                flashSeekWarning();
              }
            }}
            onTimeUpdate={(event) => {
              const video = event.currentTarget;
              if (maybeRecordProgress(video.currentTime, video.duration)) {
                video.currentTime = resumePlaybackSeconds(maxWatchedSecondsRef.current);
                flashSeekWarning();
              }
            }}
            onEnded={() => {
              const video = nativeVideoRef.current;
              if (video) {
                maybeRecordProgress(video.duration, video.duration);
              }
              if (emitCompletion("direct")) return;
              if (enforceSequentialWatchRef.current && video) {
                video.currentTime = resumePlaybackSeconds(maxWatchedSecondsRef.current);
                flashSeekWarning();
              }
            }}
          />
          {renderCompletionOverlay(replayDirectVideo)}
        </div>
        <p className="text-xs text-craft-muted">
          {watched
            ? "Video watched — you can take the Recap Quiz."
            : "Watch the video to the end before taking the Recap Quiz."}
        </p>
        {enforceSequentialWatch && (
          <p className="text-xs text-amber-700">
            Skipping ahead is disabled for required videos.
          </p>
        )}
        {showSeekWarning && (
          <p className="text-xs text-amber-700">
            Continue from the furthest point you have already watched.
          </p>
        )}
      </div>
    );
  }

  if (!id) {
    return (
      <div className="space-y-3">
        <p className="text-sm text-amber-700">
          This lesson has a video URL that could not be embedded.{" "}
          <a href={url} target="_blank" rel="noreferrer" className="font-medium underline">
            Open link
          </a>
        </p>
        {!requireFullWatch && !watched && onWatched && (
          <button
            type="button"
            onClick={() =>
              onWatched({
                source: "manual",
                durationSeconds: 0,
                watchedSeconds: 0,
              })
            }
            className="btn-secondary text-xs"
          >
            I’ve finished watching
          </button>
        )}
        {requireFullWatch && (
          <p className="text-xs text-amber-700">
            Required videos need an embeddable YouTube or direct video URL so the app can verify full playback.
          </p>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <div className="relative overflow-hidden rounded-xl border border-craft-border bg-black shadow-elevated ring-1 ring-black/20">
        <div className="relative aspect-video w-full">
          <div id={containerId} className="absolute inset-0 h-full w-full" title={title} />
          {renderCompletionOverlay(replayYouTubeVideo)}
        </div>
      </div>
      {enforceSequentialWatch && (
        <p className="text-xs text-amber-700">Skipping ahead is disabled for required videos.</p>
      )}
      {showSeekWarning && (
        <p className="text-xs text-amber-700">
          Continue from the furthest point you have already watched.
        </p>
      )}
    </div>
  );
}
