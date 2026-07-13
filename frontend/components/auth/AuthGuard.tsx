"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useAuthStore } from "@/stores/authStore";

function peekStoredAccessToken(): string | null {
  try {
    const raw = localStorage.getItem("agentcraft-auth");
    if (!raw) return null;
    const parsed = JSON.parse(raw) as { state?: { accessToken?: string | null } };
    return parsed.state?.accessToken ?? null;
  } catch {
    return null;
  }
}

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { accessToken, hasHydrated } = useAuthStore();
  const [peekToken, setPeekToken] = useState<string | null>(null);

  useEffect(() => {
    setPeekToken(peekStoredAccessToken());
  }, []);

  useEffect(() => {
    if (hasHydrated && !accessToken) {
      router.replace("/login");
    }
  }, [hasHydrated, accessToken, router]);

  const hasToken = !!accessToken || (!hasHydrated && !!peekToken);

  // Paint the shell as soon as we know a token exists (store or localStorage peek).
  if (!hasToken) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="animate-pulse text-craft-faint">Loading…</p>
      </div>
    );
  }

  return <>{children}</>;
}
