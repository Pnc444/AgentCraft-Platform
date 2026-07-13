"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { useMutation } from "@tanstack/react-query";
import Cropper, { type Area } from "react-easy-crop";
import "react-easy-crop/react-easy-crop.css";
import { removeAvatar, uploadAvatar } from "@/lib/api/auth";
import { getCroppedImage } from "@/lib/crop-image";
import { UserAvatar } from "@/components/shared/UserAvatar";
import { useAuthStore } from "@/stores/authStore";

type SaveState = "idle" | "saving" | "saved" | "error";

export function AvatarForm() {
  const user = useAuthStore((s) => s.user);
  const inputRef = useRef<HTMLInputElement>(null);

  const [draftUrl, setDraftUrl] = useState<string | null>(null);
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState<Area | null>(null);
  const [saveState, setSaveState] = useState<SaveState>("idle");
  const [error, setError] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    return () => {
      if (draftUrl) URL.revokeObjectURL(draftUrl);
    };
  }, [draftUrl]);

  useEffect(() => {
    if (saveState !== "saved") return;
    const t = window.setTimeout(() => setSaveState("idle"), 2200);
    return () => window.clearTimeout(t);
  }, [saveState]);

  useEffect(() => {
    if (saveState !== "error") return;
    const t = window.setTimeout(() => {
      setSaveState("idle");
      setError(null);
    }, 2800);
    return () => window.clearTimeout(t);
  }, [saveState]);

  // Lock page scroll while the crop modal is open
  useEffect(() => {
    if (!draftUrl) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev;
    };
  }, [draftUrl]);

  const onCropComplete = useCallback((_: Area, pixels: Area) => {
    setCroppedAreaPixels(pixels);
  }, []);

  function clearDraft() {
    if (draftUrl) URL.revokeObjectURL(draftUrl);
    setDraftUrl(null);
    setCrop({ x: 0, y: 0 });
    setZoom(1);
    setCroppedAreaPixels(null);
    if (inputRef.current) inputRef.current.value = "";
  }

  const uploadMutation = useMutation({
    mutationFn: async () => {
      if (!draftUrl || !croppedAreaPixels) {
        throw new Error("Nothing to save");
      }
      const blob = await getCroppedImage(draftUrl, croppedAreaPixels);
      const file = new File([blob], "avatar.jpg", { type: "image/jpeg" });
      return uploadAvatar(file);
    },
    onMutate: () => {
      setSaveState("saving");
      setError(null);
    },
    onSuccess: () => {
      clearDraft();
      setSaveState("saved");
      setError(null);
    },
    onError: () => {
      setSaveState("error");
      setError("Try again later");
    },
  });

  const removeMutation = useMutation({
    mutationFn: () => removeAvatar(),
    onSuccess: () => {
      setSaveState("idle");
      setError(null);
    },
    onError: () => {
      setSaveState("error");
      setError("Try again later");
    },
  });

  function onFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    if (file.size > 8 * 1024 * 1024) {
      setError("Image must be 8MB or smaller before crop.");
      setSaveState("error");
      return;
    }
    // HEIC often won't render in-browser for cropping
    if (/heic|heif/i.test(file.type) || /\.heic$|\.heif$/i.test(file.name)) {
      setError("Use JPEG, PNG, or WebP for cropping.");
      setSaveState("error");
      if (inputRef.current) inputRef.current.value = "";
      return;
    }
    if (draftUrl) URL.revokeObjectURL(draftUrl);
    const url = URL.createObjectURL(file);
    setDraftUrl(url);
    setCrop({ x: 0, y: 0 });
    setZoom(1);
    setCroppedAreaPixels(null);
    setSaveState("idle");
    setError(null);
  }

  const busy = uploadMutation.isPending || removeMutation.isPending;
  const editing = !!draftUrl;

  let saveLabel = "Save";
  if (saveState === "saving") saveLabel = "Saving…";
  else if (saveState === "saved") saveLabel = "Saved!";
  else if (saveState === "error") saveLabel = "Try again later";

  const cropModal =
    mounted &&
    editing &&
    draftUrl &&
    createPortal(
      <div
        className="fixed inset-0 z-[100000] flex items-center justify-center bg-black/70 p-4 backdrop-blur-sm"
        role="dialog"
        aria-modal="true"
        aria-label="Crop profile photo"
      >
        <div className="w-full max-w-md rounded-2xl border border-craft-border bg-craft-surface p-4 shadow-float">
          <h3 className="text-sm font-semibold text-craft-ink">Crop photo</h3>
          <p className="mt-1 text-xs text-craft-muted">Drag to move · scroll or slider to zoom</p>

          <div className="relative mt-4 h-72 w-full overflow-hidden rounded-xl bg-slate-900">
            <Cropper
              image={draftUrl}
              crop={crop}
              zoom={zoom}
              minZoom={1}
              maxZoom={3}
              aspect={1}
              cropShape="round"
              showGrid={false}
              objectFit="horizontal-cover"
              onCropChange={setCrop}
              onZoomChange={setZoom}
              onCropComplete={onCropComplete}
              style={{
                containerStyle: { background: "#0f172a" },
                mediaStyle: { opacity: 1 },
                cropAreaStyle: {
                  border: "2px solid rgba(34, 211, 238, 0.85)",
                  boxShadow: "0 0 0 9999px rgba(15, 23, 42, 0.65)",
                  color: "rgba(15, 23, 42, 0.65)",
                },
              }}
            />
          </div>

          <label className="mt-4 block">
            <span className="mb-1 block text-[11px] font-medium uppercase tracking-wide text-craft-faint">
              Zoom
            </span>
            <input
              type="range"
              min={1}
              max={3}
              step={0.05}
              value={zoom}
              onChange={(e) => setZoom(Number(e.target.value))}
              className="w-full accent-cyan-500"
              disabled={busy}
            />
          </label>

          <div className="mt-4 flex gap-2">
            <button
              type="button"
              disabled={busy || !croppedAreaPixels || saveState === "saved"}
              onClick={() => {
                if (saveState === "error") {
                  setSaveState("idle");
                  setError(null);
                }
                uploadMutation.mutate();
              }}
              className="btn-primary flex-1 px-4 py-2 text-xs"
            >
              {saveLabel}
            </button>
            <button
              type="button"
              disabled={busy}
              onClick={() => {
                clearDraft();
                setSaveState("idle");
                setError(null);
              }}
              className="btn-secondary flex-1 px-4 py-2 text-xs"
            >
              Cancel
            </button>
          </div>
          {error && saveState === "error" && (
            <p className="mt-2 text-center text-xs text-amber-700 dark:text-amber-300">{error}</p>
          )}
        </div>
      </div>,
      document.body
    );

  return (
    <div className="card flex h-full flex-col space-y-3 p-4">
      <div className="flex items-center justify-between gap-2">
        <h2 className="text-sm font-semibold text-craft-ink">Profile photo</h2>
        {saveState === "saved" && !editing && (
          <p className="text-xs text-emerald-700 dark:text-emerald-300">Saved!</p>
        )}
        {error && saveState === "error" && !editing && (
          <p className="text-xs text-amber-700 dark:text-amber-300">{error}</p>
        )}
      </div>

      <div className="flex flex-1 flex-col items-center justify-center gap-3 py-2">
        <UserAvatar size="lg" />
        <p className="text-center text-xs text-craft-muted">
          JPEG, PNG, WebP · crop before saving
        </p>
      </div>

      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp,image/gif"
        className="hidden"
        onChange={onFileChange}
      />

      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          disabled={busy || editing}
          onClick={() => {
            setSaveState("idle");
            setError(null);
            inputRef.current?.click();
          }}
          className="btn-primary flex-1 px-4 py-2 text-xs"
        >
          {saveState === "saved"
            ? "Saved!"
            : user?.avatar
              ? "Change photo"
              : "Choose photo"}
        </button>
        {user?.avatar && (
          <button
            type="button"
            disabled={busy || editing}
            onClick={() => removeMutation.mutate()}
            className="btn-secondary flex-1 px-4 py-2 text-xs"
          >
            {removeMutation.isPending ? "…" : "Remove"}
          </button>
        )}
      </div>

      {cropModal}
    </div>
  );
}
