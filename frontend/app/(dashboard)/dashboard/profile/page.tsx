"use client";

import { FormEvent, useEffect, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import clsx from "clsx";
import { ChevronDown } from "lucide-react";
import { changePassword, updateProfile } from "@/lib/api/auth";
import { AvatarForm } from "@/components/dashboard/AvatarForm";
import { BadgeIcon } from "@/components/dashboard/BadgeIcon";
import { UserAvatar } from "@/components/shared/UserAvatar";
import { Reveal } from "@/components/shared/Reveal";
import { getDashboardStats } from "@/lib/api/courses";
import { useAuthStore } from "@/stores/authStore";
import type { Badge } from "@/types";

type Tab = "profile" | "settings";

export default function ProfilePage() {
  const user = useAuthStore((s) => s.user);
  const [tab, setTab] = useState<Tab>("profile");

  const { data: stats } = useQuery({ queryKey: ["dashboard-stats"], queryFn: getDashboardStats });

  const equippedBadge = stats?.badges.find((b) => b.equipped);

  return (
    <div className="mx-auto max-w-5xl">
      <Reveal>
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-craft-ink">Profile</h1>
            <p className="mt-0.5 text-sm text-craft-muted">Account and progress</p>
          </div>
          <div className="flex rounded-full border border-craft-border bg-craft-surface p-0.5 text-sm font-semibold">
            {(["profile", "settings"] as Tab[]).map((t) => (
              <button
                key={t}
                type="button"
                onClick={() => setTab(t)}
                className={clsx(
                  "rounded-full px-3.5 py-1.5 capitalize transition",
                  tab === t
                    ? "bg-cyan-500 text-white"
                    : "text-craft-muted hover:text-craft-ink"
                )}
              >
                {t}
              </button>
            ))}
          </div>
        </div>
      </Reveal>

      {tab === "profile" && (
        <div className="mt-5 space-y-4">
          <Reveal delay={60} variant="scale">
            <div className="card card-interactive flex flex-wrap items-center gap-4 p-4">
              {user?.avatar ? (
                <UserAvatar size="lg" />
              ) : equippedBadge ? (
                <span className="flex h-16 w-16 items-center justify-center rounded-full bg-cyan-50 text-cyan-600 dark:text-cyan-400">
                  <BadgeIcon name={equippedBadge.icon} className="h-7 w-7" />
                </span>
              ) : (
                <UserAvatar size="lg" />
              )}
              <div className="min-w-0 flex-1">
                <h2 className="truncate text-base font-semibold text-craft-ink">{user?.username}</h2>
                <p className="truncate text-sm text-craft-muted">{user?.email}</p>
                {equippedBadge && (
                  <p className="mt-1 flex items-center gap-1 text-xs font-medium text-cyan-600 dark:text-cyan-400">
                    <BadgeIcon name={equippedBadge.icon} className="h-3 w-3" />
                    {equippedBadge.name}
                  </p>
                )}
              </div>
              <div className="flex w-full gap-2 sm:ml-auto sm:w-auto">
                <StatChip label="Done" value={stats?.lessons_completed ?? 0} />
                <StatChip label="Active" value={stats?.lessons_in_progress ?? 0} />
                <StatChip label="Progress" value={`${stats?.overall_progress_pct ?? 0}%`} />
              </div>
            </div>
          </Reveal>

          <Reveal delay={100}>
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-craft-ink">Badges</h2>
              <p className="text-sm text-craft-muted">
                {stats?.badges_unlocked ?? 0} of {stats?.badges_total ?? 0} unlocked
              </p>
            </div>
          </Reveal>
          <BadgesGrid badges={stats?.badges ?? []} />
        </div>
      )}

      {tab === "settings" && (
        <div className="mt-5 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <Reveal delay={60}>
            <AvatarForm />
          </Reveal>
          <Reveal delay={120}>
            <ProfileForm />
          </Reveal>
          <Reveal delay={180}>
            <PasswordForm />
          </Reveal>
        </div>
      )}
    </div>
  );
}

function StatChip({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="min-w-0 flex-1 rounded-xl border border-craft-border bg-craft-soft px-3 py-2 text-center sm:flex-none sm:min-w-[4.5rem]">
      <p className="text-base font-bold tabular-nums text-craft-ink">{value}</p>
      <p className="text-[10px] font-medium uppercase tracking-wide text-craft-muted">{label}</p>
    </div>
  );
}

/** First row size matches grid: 1 / sm:2 / lg:4 */
function useBadgeRowSize() {
  const [rowSize, setRowSize] = useState(4);

  useEffect(() => {
    const mqLg = window.matchMedia("(min-width: 1024px)");
    const mqSm = window.matchMedia("(min-width: 640px)");
    function update() {
      if (mqLg.matches) setRowSize(4);
      else if (mqSm.matches) setRowSize(2);
      else setRowSize(1);
    }
    update();
    mqLg.addEventListener("change", update);
    mqSm.addEventListener("change", update);
    return () => {
      mqLg.removeEventListener("change", update);
      mqSm.removeEventListener("change", update);
    };
  }, []);

  return rowSize;
}

function BadgesGrid({ badges }: { badges: Badge[] }) {
  const rowSize = useBadgeRowSize();
  const [expanded, setExpanded] = useState(false);
  const hasMore = badges.length > rowSize;
  const visible = expanded || !hasMore ? badges : badges.slice(0, rowSize);

  return (
    <div className="mt-4">
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {visible.map((badge, i) => (
          <Reveal key={badge.id} delay={Math.min(i * 50, 200)} variant="scale">
            <div
              className={clsx(
                "card card-interactive p-4 text-center",
                badge.unlocked ? "border-cyan-400/30" : "opacity-50"
              )}
              title={badge.description}
            >
              <BadgeIcon
                name={badge.icon}
                className={
                  "mx-auto h-8 w-8 " +
                  (badge.unlocked ? "text-cyan-600 dark:text-cyan-400" : "text-craft-muted")
                }
              />
              <p className="mt-2 text-sm font-medium text-craft-ink">{badge.name}</p>
              <p className="mt-1 text-xs text-craft-muted">{badge.description}</p>
              {badge.equipped && (
                <p className="mt-2 text-xs font-semibold text-cyan-600 dark:text-cyan-400">
                  Equipped
                </p>
              )}
            </div>
          </Reveal>
        ))}
      </div>

      {hasMore && (
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          aria-expanded={expanded}
          className="mt-3 flex w-full items-center justify-center gap-1.5 rounded-xl py-2.5 text-sm font-medium text-craft-muted transition hover:bg-craft-soft hover:text-craft-ink"
        >
          {expanded ? "See less" : "See more badges"}
          <ChevronDown
            className={clsx("h-4 w-4 transition-transform", expanded && "rotate-180")}
          />
        </button>
      )}
    </div>
  );
}

function FormMessage({ message, error }: { message: string | null; error: string | null }) {
  if (message) return <p className="text-xs text-emerald-700">{message}</p>;
  if (error) return <p className="text-xs text-amber-700">{error}</p>;
  return null;
}

function ProfileForm() {
  const user = useAuthStore((s) => s.user);
  const queryClient = useQueryClient();
  const [firstName, setFirstName] = useState(user?.first_name ?? "");
  const [lastName, setLastName] = useState(user?.last_name ?? "");
  const [email, setEmail] = useState(user?.email ?? "");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: () => updateProfile({ first_name: firstName, last_name: lastName, email }),
    onSuccess: () => {
      setMessage("Saved.");
      setError(null);
      queryClient.invalidateQueries({ queryKey: ["dashboard-stats"] });
    },
    onError: (err) => {
      setError(err instanceof Error ? err.message : "Update failed");
      setMessage(null);
    },
  });

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    mutation.mutate();
  }

  return (
    <form onSubmit={handleSubmit} className="card flex h-full flex-col space-y-3 p-4">
      <div className="flex items-center justify-between gap-2">
        <h2 className="text-sm font-semibold text-craft-ink">Details</h2>
        <FormMessage message={message} error={error} />
      </div>
      <div className="grid flex-1 grid-cols-2 gap-2 content-start">
        <Field label="First name" id="firstName">
          <input
            id="firstName"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            placeholder="First"
            className="input-field px-3 py-2 text-sm"
          />
        </Field>
        <Field label="Last name" id="lastName">
          <input
            id="lastName"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            placeholder="Last"
            className="input-field px-3 py-2 text-sm"
          />
        </Field>
        <div className="col-span-2">
          <Field label="Email" id="email">
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              className="input-field px-3 py-2 text-sm"
            />
          </Field>
        </div>
      </div>
      <button type="submit" disabled={mutation.isPending} className="btn-primary px-4 py-2 text-xs">
        {mutation.isPending ? "Saving…" : "Save"}
      </button>
    </form>
  );
}

function PasswordForm() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: () => changePassword(currentPassword, newPassword),
    onSuccess: () => {
      setMessage("Password updated.");
      setError(null);
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    },
    onError: (err) => {
      setError(err instanceof Error ? err.message : "Password change failed");
      setMessage(null);
    },
  });

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      setMessage(null);
      return;
    }
    mutation.mutate();
  }

  return (
    <form onSubmit={handleSubmit} className="card flex h-full flex-col space-y-3 p-4">
      <div className="flex items-center justify-between gap-2">
        <h2 className="text-sm font-semibold text-craft-ink">Password</h2>
        <FormMessage message={message} error={error} />
      </div>
      <div className="flex flex-1 flex-col gap-2">
        <Field label="Current" id="currentPassword">
          <input
            id="currentPassword"
            type="password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            required
            className="input-field px-3 py-2 text-sm"
          />
        </Field>
        <Field label="New" id="newPassword">
          <input
            id="newPassword"
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
            className="input-field px-3 py-2 text-sm"
          />
        </Field>
        <Field label="Confirm" id="confirmPassword">
          <input
            id="confirmPassword"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            className="input-field px-3 py-2 text-sm"
          />
        </Field>
      </div>
      <button type="submit" disabled={mutation.isPending} className="btn-primary px-4 py-2 text-xs">
        {mutation.isPending ? "Updating…" : "Update"}
      </button>
    </form>
  );
}

function Field({
  label,
  id,
  children,
}: {
  label: string;
  id: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label htmlFor={id} className="mb-1 block text-xs font-medium text-craft-muted">
        {label}
      </label>
      {children}
    </div>
  );
}
