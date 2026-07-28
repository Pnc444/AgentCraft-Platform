"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
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
import { usePageChrome } from "@/stores/pageChrome";
import type { Badge } from "@/types";

type Tab = "profile" | "settings";

export default function ProfilePage() {
  const user = useAuthStore((s) => s.user);
  const setChrome = usePageChrome((s) => s.setChrome);
  const clearChrome = usePageChrome((s) => s.clearChrome);
  const [tab, setTab] = useState<Tab>("profile");

  useEffect(() => {
    if (typeof window === "undefined") return;
    const params = new URLSearchParams(window.location.search);
    if (params.get("tab") === "settings") setTab("settings");
  }, []);

  const { data: stats } = useQuery({ queryKey: ["dashboard-stats"], queryFn: getDashboardStats });

  const equippedBadge = stats?.badges.find((b) => b.equipped);

  const handleTabChange = useCallback((id: string) => {
    setTab(id as Tab);
  }, []);

  useEffect(() => {
    setChrome({
      title: "Profile",
      subtitle: tab === "settings" ? "Account settings" : "Account and progress",
      showAskTutor: false,
      onAskTutor: null,
      headerTabs: [
        { id: "profile", label: "Profile" },
        { id: "settings", label: "Settings" },
      ],
      activeTab: tab,
      onTabChange: handleTabChange,
    });
    return () => clearChrome();
  }, [clearChrome, handleTabChange, setChrome, tab]);

  return (
    <div className="mx-auto max-w-4xl">
      <div className="mb-4 flex rounded-full border border-craft-border bg-craft-surface p-0.5 text-sm font-medium sm:hidden">
        {(["profile", "settings"] as Tab[]).map((t) => (
          <button
            key={t}
            type="button"
            onClick={() => setTab(t)}
            className={clsx(
              "flex-1 rounded-full px-3 py-2 capitalize transition",
              tab === t
                ? "bg-craft-soft text-craft-ink"
                : "text-craft-muted hover:text-craft-ink"
            )}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === "profile" && (
        <div className="space-y-4">
          <Reveal delay={60} variant="scale">
            <div className="card flex flex-wrap items-center gap-4 p-4">
              {user?.avatar ? (
                <UserAvatar size="lg" />
              ) : equippedBadge ? (
                <span className="flex h-16 w-16 items-center justify-center rounded-full bg-violet-50 text-violet-600 dark:text-violet-400">
                  <BadgeIcon name={equippedBadge.icon} className="h-7 w-7" />
                </span>
              ) : (
                <UserAvatar size="lg" />
              )}
              <div className="min-w-0 flex-1">
                <h2 className="truncate text-base font-semibold text-craft-ink">{user?.username}</h2>
                <p className="truncate text-sm text-craft-muted">{user?.email}</p>
                {equippedBadge && (
                  <p className="mt-1 flex items-center gap-1 text-xs font-medium text-violet-600 dark:text-violet-400">
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
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <Reveal delay={60}>
            <AvatarForm />
          </Reveal>
          <div className="flex flex-col gap-3 md:col-span-1 lg:col-span-2">
            <Reveal delay={120}>
              <SettingsDisclosure label="Details">
                <ProfileForm />
              </SettingsDisclosure>
            </Reveal>
            <Reveal delay={180}>
              <SettingsDisclosure label="Change password">
                <PasswordForm />
              </SettingsDisclosure>
            </Reveal>
          </div>
        </div>
      )}
    </div>
  );
}

function SettingsDisclosure({
  label,
  children,
  defaultOpen = false,
}: {
  label: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  const panelId = `settings-${label.toLowerCase().replace(/\s+/g, "-")}`;

  return (
    <div className="card overflow-hidden p-0">
      <button
        type="button"
        aria-expanded={open}
        aria-controls={panelId}
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center justify-between gap-3 px-4 py-3.5 text-left text-sm font-semibold text-craft-ink transition hover:bg-craft-soft"
      >
        {label}
        <ChevronDown
          className={clsx(
            "h-4 w-4 shrink-0 text-craft-faint transition-transform",
            open && "rotate-180"
          )}
        />
      </button>
      {open ? (
        <div id={panelId} className="border-t border-craft-border px-4 pb-4 pt-3">
          {children}
        </div>
      ) : null}
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
      <div className="grid auto-rows-fr gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {visible.map((badge, i) => (
          <Reveal
            key={badge.id}
            className="h-full"
            delay={Math.min(i * 50, 200)}
            variant="scale"
          >
            <div
              className={clsx(
                "card flex h-full min-h-[11.5rem] flex-col p-4 text-center",
                badge.unlocked ? "border-violet-400/30" : "opacity-50"
              )}
              title={badge.description}
            >
              <BadgeIcon
                name={badge.icon}
                className={
                  "mx-auto h-8 w-8 shrink-0 " +
                  (badge.unlocked ? "text-violet-600 dark:text-violet-400" : "text-craft-muted")
                }
              />
              <p className="mt-2 line-clamp-2 text-sm font-medium text-craft-ink">{badge.name}</p>
              <p className="mt-1 line-clamp-3 text-xs text-craft-muted">{badge.description}</p>
              <div className="mt-auto pt-2">
                {badge.equipped && (
                  <p className="text-xs font-semibold text-violet-600 dark:text-violet-400">
                    Equipped
                  </p>
                )}
              </div>
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
  const [username, setUsername] = useState(user?.username ?? "");
  const [firstName, setFirstName] = useState(user?.first_name ?? "");
  const [lastName, setLastName] = useState(user?.last_name ?? "");
  const [email, setEmail] = useState(user?.email ?? "");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setUsername(user?.username ?? "");
    setFirstName(user?.first_name ?? "");
    setLastName(user?.last_name ?? "");
    setEmail(user?.email ?? "");
  }, [user?.username, user?.first_name, user?.last_name, user?.email]);

  const mutation = useMutation({
    mutationFn: () =>
      updateProfile({
        username: username.trim(),
        first_name: firstName,
        last_name: lastName,
        email,
      }),
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
    <form onSubmit={handleSubmit} className="flex flex-col space-y-3">
      <FormMessage message={message} error={error} />
      <div className="grid grid-cols-2 content-start gap-2">
        <div className="col-span-2">
          <Field label="Username" id="username">
            <input
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              required
              autoComplete="username"
              maxLength={150}
              className="input-field px-3 py-2 text-sm"
            />
          </Field>
        </div>
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
    <form onSubmit={handleSubmit} className="flex flex-col space-y-3">
      <FormMessage message={message} error={error} />
      <div className="flex flex-col gap-2">
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
