"use client";

import clsx from "clsx";
import { useAuthStore } from "@/stores/authStore";

interface UserAvatarProps {
  size?: "sm" | "md" | "lg";
  className?: string;
  /** Override store user (e.g. preview). */
  src?: string | null;
  username?: string;
}

const sizeCls = {
  sm: "h-8 w-8 text-xs",
  md: "h-9 w-9 text-sm",
  lg: "h-16 w-16 text-xl",
};

export function UserAvatar({ size = "sm", className, src, username }: UserAvatarProps) {
  const user = useAuthStore((s) => s.user);
  const avatar = src !== undefined ? src : user?.avatar;
  const name = username ?? user?.username ?? "U";
  const initials = name.slice(0, 2).toUpperCase();

  if (avatar) {
    return (
      // eslint-disable-next-line @next/next/no-img-element
      <img
        src={avatar}
        alt=""
        className={clsx(
          "shrink-0 rounded-full object-cover ring-1 ring-cyan-400/30",
          sizeCls[size],
          className
        )}
      />
    );
  }

  return (
    <span
      className={clsx(
        "flex shrink-0 items-center justify-center rounded-full bg-cyan-500/15 font-bold text-cyan-700 dark:text-cyan-300",
        sizeCls[size],
        className
      )}
      aria-hidden
    >
      {initials}
    </span>
  );
}
