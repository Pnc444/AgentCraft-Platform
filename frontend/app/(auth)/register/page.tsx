"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { register } from "@/lib/api/auth";
import { Reveal } from "@/components/shared/Reveal";

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

  return (
    <Reveal variant="scale" className="w-full max-w-md">
      <div className="card w-full p-8 shadow-elevated">
        <h1 className="text-2xl font-bold text-craft-ink">Create your account</h1>
        <p className="mt-1 text-sm text-craft-muted">Start learning AI agents from zero.</p>

        {error && (
          <p className="mt-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-2 text-sm text-amber-700">
            {error}
          </p>
        )}

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div>
            <label htmlFor="username" className="mb-1 block text-sm font-medium text-craft-muted">
              Username
            </label>
            <input
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Choose a username"
              required
              className="input-field"
            />
          </div>
          <div>
            <label htmlFor="email" className="mb-1 block text-sm font-medium text-craft-muted">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              className="input-field"
            />
          </div>
          <div>
            <label htmlFor="password" className="mb-1 block text-sm font-medium text-craft-muted">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="At least 8 characters"
              required
              className="input-field"
            />
          </div>
          <div>
            <label
              htmlFor="passwordConfirm"
              className="mb-1 block text-sm font-medium text-craft-muted"
            >
              Confirm password
            </label>
            <input
              id="passwordConfirm"
              type="password"
              value={passwordConfirm}
              onChange={(e) => setPasswordConfirm(e.target.value)}
              placeholder="Repeat your password"
              required
              className="input-field"
            />
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? "Creating account…" : "Create account"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-craft-muted">
          Already have an account?{" "}
          <Link href="/login" className="font-semibold text-cyan-600 hover:underline dark:text-cyan-400">
            Log in
          </Link>
        </p>
      </div>
    </Reveal>
  );
}
