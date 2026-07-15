"use client";

import { useEffect, useId, useRef } from "react";

interface LessonVideoProps {
  url: string;
  title?: string;
  onWatched?: () => void;
  watched?: boolean;
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
      ) => { destroy?: () => void };
      PlayerState?: { ENDED: number };
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
}: LessonVideoProps) {
  const id = youtubeVideoId(url);
  const reactId = useId().replace(/:/g, "");
  const containerId = `yt-player-${reactId}`;
  const playerRef = useRef<{ destroy?: () => void } | null>(null);
  const watchedRef = useRef(watched);

  useEffect(() => {
    watchedRef.current = watched;
  }, [watched]);

  useEffect(() => {
    if (!id || watched) return;
    let cancelled = false;

    loadYouTubeApi().then(() => {
      if (cancelled || !window.YT?.Player) return;
      const ended = window.YT.PlayerState?.ENDED ?? 0;
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
            if (event.data === ended && !watchedRef.current) {
              onWatched?.();
            }
          },
        },
      });
    });

    return () => {
      cancelled = true;
      try {
        playerRef.current?.destroy?.();
      } catch {
        /* ignore */
      }
      playerRef.current = null;
    };
  }, [containerId, id, onWatched, watched]);

  if (isDirectVideoUrl(url)) {
    return (
      <div className="space-y-2">
        <div className="overflow-hidden rounded-xl border border-craft-border bg-black shadow-elevated ring-1 ring-black/20">
          {/* eslint-disable-next-line jsx-a11y/media-has-caption */}
          <video
            className="aspect-video w-full"
            src={url}
            controls
            playsInline
            preload="metadata"
            title={title}
            onEnded={() => {
              if (!watchedRef.current) onWatched?.();
            }}
          />
        </div>
        <p className="text-xs text-craft-muted">
          {watched
            ? "Video watched — you can take the Recap Quiz."
            : "Watch the video to the end before taking the Recap Quiz."}
        </p>
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
        {!watched && onWatched && (
          <button type="button" onClick={onWatched} className="btn-secondary text-xs">
            I’ve finished watching
          </button>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <div className="overflow-hidden rounded-xl border border-craft-border bg-black shadow-elevated ring-1 ring-black/20">
        <div className="relative aspect-video w-full">
          {watched ? (
            <iframe
              className="absolute inset-0 h-full w-full"
              src={`https://www.youtube-nocookie.com/embed/${id}`}
              title={title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowFullScreen
              loading="lazy"
              referrerPolicy="strict-origin-when-cross-origin"
            />
          ) : (
            <div id={containerId} className="absolute inset-0 h-full w-full" title={title} />
          )}
        </div>
      </div>
      <p className="text-xs text-craft-muted">
        {watched
          ? "Video watched — you can take the Recap Quiz."
          : "Watch the video to the end before taking the Recap Quiz."}
      </p>
    </div>
  );
}
