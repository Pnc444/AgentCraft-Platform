"use client";

import { FormEvent, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import clsx from "clsx";
import { CircleUserRound } from "lucide-react";
import { changePassword, updateProfile } from "@/lib/api/auth";
import { BadgeIcon } from "@/components/dashboard/BadgeIcon";
import { getDashboardStats } from "@/lib/api/courses";
import { useAuthStore } from "@/stores/authStore";

type Tab = "profile" | "settings";

const inputCls =
  "w-full rounded-lg border border-white/10 bg-craft-950 px-4 py-2.5 text-white placeholder:text-slate-600 focus:border-craft-accent focus:outline-none";

export default function ProfilePage() {
  const user = useAuthStore((s) => s.user);
  const [tab, setTab] = useState<Tab>("profile");

  const { data: stats } = useQuery({ queryKey: ["dashboard-stats"], queryFn: getDashboardStats });

  const equippedBadge = stats?.badges.find((b) => b.equipped);

  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="text-2xl font-bold text-white">Your Profile</h1>
      <p className="mt-1 text-slate-400">Track your journey and manage your account</p>

      <div className="mt-6 flex gap-2 border-b border-white/10">
        {(["profile", "settings"] as Tab[]).map((t) => (
          <button
            key={t}
            type="button"
            onClick={() => setTab(t)}
            className={clsx(
              "border-b-2 px-4 py-2.5 text-sm font-medium capitalize transition-colors",
              tab === t
                ? "border-craft-accent text-white"
                : "border-transparent text-slate-400 hover:text-white"
            )}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === "profile" && (
        <div className="mt-8 space-y-8">
          <div className="flex flex-wrap items-center gap-5 rounded-2xl border border-white/10 bg-craft-900/60 p-6">
            <span className="flex h-16 w-16 items-center justify-center rounded-full bg-craft-accent/20 text-craft-glow">
              {equippedBadge ? (
                <BadgeIcon name={equippedBadge.icon} className="h-8 w-8" />
              ) : (
                <CircleUserRound className="h-8 w-8" />
              )}
            </span>
            <div>
              <h2 className="text-lg font-semibold text-white">{user?.username}</h2>
              <p className="text-sm text-slate-400">{user?.email}</p>
              {equippedBadge && (
                <p className="mt-1 flex items-center gap-1.5 text-xs text-craft-glow">
                  <BadgeIcon name={equippedBadge.icon} className="h-3.5 w-3.5" />
                  {equippedBadge.name} equipped
                </p>
              )}
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-3">
            <StatCard label="Lessons completed" value={stats?.lessons_completed ?? 0} />
            <StatCard label="In progress" value={stats?.lessons_in_progress ?? 0} />
            <StatCard label="Overall progress" value={`${stats?.overall_progress_pct ?? 0}%`} />
          </div>

          <div>
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-white">Badges</h2>
              <p className="text-sm text-slate-500">
                {stats?.badges_unlocked ?? 0} of {stats?.badges_total ?? 0} unlocked
              </p>
            </div>
            <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              {stats?.badges.map((badge) => (
                <div
                  key={badge.id}
                  className={clsx(
                    "rounded-xl border p-4 text-center",
                    badge.unlocked
                      ? "border-craft-accent/40 bg-craft-accent/5"
                      : "border-white/10 bg-craft-900/40 opacity-50"
                  )}
                  title={badge.description}
                >
                  <BadgeIcon
                    name={badge.icon}
                    className={"mx-auto h-8 w-8 " + (badge.unlocked ? "text-craft-glow" : "text-slate-600")}
                  />
                  <p className="mt-2 text-sm font-medium text-white">{badge.name}</p>
                  <p className="mt-1 text-xs text-slate-500">{badge.description}</p>
                  {badge.equipped && (
                    <p className="mt-2 text-xs font-medium text-craft-glow">Equipped</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {tab === "settings" && (
        <div className="mt-8 grid gap-8 lg:grid-cols-2">
          <ProfileForm />
          <PasswordForm />
        </div>
      )}
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-craft-900/60 p-6">
      <p className="text-3xl font-bold text-white">{value}</p>
      <p className="mt-1 text-sm text-slate-400">{label}</p>
    </div>
  );
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
      setMessage("Profile updated successfully.");
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
    <form onSubmit={handleSubmit} className="rounded-2xl border border-white/10 bg-craft-900/60 p-6">
      <h2 className="text-lg font-semibold text-white">Profile details</h2>
      {message && <p className="mt-3 text-sm text-emerald-300">{message}</p>}
      {error && <p className="mt-3 text-sm text-red-300">{error}</p>}
      <div className="mt-4 space-y-4">
        <div>
          <label htmlFor="firstName" className="mb-1 block text-sm text-slate-300">First name</label>
          <input id="firstName" value={firstName} onChange={(e) => setFirstName(e.target.value)} placeholder="First name" className={inputCls} />
        </div>
        <div>
          <label htmlFor="lastName" className="mb-1 block text-sm text-slate-300">Last name</label>
          <input id="lastName" value={lastName} onChange={(e) => setLastName(e.target.value)} placeholder="Last name" className={inputCls} />
        </div>
        <div>
          <label htmlFor="email" className="mb-1 block text-sm text-slate-300">Email</label>
          <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required className={inputCls} />
        </div>
        <button
          type="submit"
          disabled={mutation.isPending}
          className="rounded-lg bg-craft-accent px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-indigo-500 disabled:opacity-50"
        >
          {mutation.isPending ? "Saving…" : "Save changes"}
        </button>
      </div>
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
      setMessage("Password updated successfully.");
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
      setError("New passwords do not match.");
      setMessage(null);
      return;
    }
    mutation.mutate();
  }

  return (
    <form onSubmit={handleSubmit} className="rounded-2xl border border-white/10 bg-craft-900/60 p-6">
      <h2 className="text-lg font-semibold text-white">Change password</h2>
      {message && <p className="mt-3 text-sm text-emerald-300">{message}</p>}
      {error && <p className="mt-3 text-sm text-red-300">{error}</p>}
      <div className="mt-4 space-y-4">
        <div>
          <label htmlFor="currentPassword" className="mb-1 block text-sm text-slate-300">Current password</label>
          <input id="currentPassword" type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} required className={inputCls} />
        </div>
        <div>
          <label htmlFor="newPassword" className="mb-1 block text-sm text-slate-300">New password</label>
          <input id="newPassword" type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required className={inputCls} />
        </div>
        <div>
          <label htmlFor="confirmPassword" className="mb-1 block text-sm text-slate-300">Confirm new password</label>
          <input id="confirmPassword" type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required className={inputCls} />
        </div>
        <button
          type="submit"
          disabled={mutation.isPending}
          className="rounded-lg bg-craft-accent px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-indigo-500 disabled:opacity-50"
        >
          {mutation.isPending ? "Updating…" : "Update password"}
        </button>
      </div>
    </form>
  );
}
