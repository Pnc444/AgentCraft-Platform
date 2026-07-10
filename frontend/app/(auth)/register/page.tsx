"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { register } from "@/lib/api/auth";

export default function RegisterPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (password !== passwordConfirm) {
      setError("Passwords do not match.");
      return;
    }
    setLoading(true);
    try {
      await register(username, email, password, passwordConfirm);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
      setLoading(false);
    }
  }

  const inputCls =
    "w-full rounded-lg border border-white/10 bg-craft-950 px-4 py-2.5 text-white placeholder:text-slate-600 focus:border-craft-accent focus:outline-none";

  return (
    <div className="w-full max-w-md rounded-2xl border border-white/10 bg-craft-900/60 p-8">
        <h1 className="text-2xl font-bold text-white">Create your account</h1>
        <p className="mt-1 text-sm text-slate-400">Start learning AI agents from zero.</p>

        {error && (
          <p className="mt-4 rounded-lg border border-red-500/30 bg-red-950/30 px-4 py-2 text-sm text-red-300">
            {error}
          </p>
        )}

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div>
            <label htmlFor="username" className="mb-1 block text-sm text-slate-300">Username</label>
            <input id="username" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Choose a username" required className={inputCls} />
          </div>
          <div>
            <label htmlFor="email" className="mb-1 block text-sm text-slate-300">Email</label>
            <input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" required className={inputCls} />
          </div>
          <div>
            <label htmlFor="password" className="mb-1 block text-sm text-slate-300">Password</label>
            <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="At least 8 characters" required className={inputCls} />
          </div>
          <div>
            <label htmlFor="passwordConfirm" className="mb-1 block text-sm text-slate-300">Confirm password</label>
            <input id="passwordConfirm" type="password" value={passwordConfirm} onChange={(e) => setPasswordConfirm(e.target.value)} placeholder="Repeat your password" required className={inputCls} />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-craft-accent px-4 py-2.5 font-medium text-white transition-colors hover:bg-indigo-500 disabled:opacity-50"
          >
            {loading ? "Creating account…" : "Create account"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-slate-400">
          Already have an account?{" "}
          <Link href="/login" className="text-craft-glow hover:underline">Log in</Link>
        </p>
      </div>
  );
}
