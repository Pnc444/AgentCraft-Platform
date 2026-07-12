"use client";

import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";

/** Sends authenticated visitors from `/` to the dashboard, unless they opted into the landing page. */
export function AuthHomeRedirect() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const accessToken = useAuthStore((s) => s.accessToken);
  const hasHydrated = useAuthStore((s) => s.hasHydrated);
  const stayOnLanding = searchParams.get("landing") === "1";

  useEffect(() => {
    if (hasHydrated && accessToken && !stayOnLanding) {
      router.replace("/dashboard");
    }
  }, [accessToken, hasHydrated, router, stayOnLanding]);

  return null;
}
