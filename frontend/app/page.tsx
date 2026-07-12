import { Suspense } from "react";
import { SiteHeader } from "@/components/landing/SiteHeader";
import { Hero } from "@/components/landing/Hero";
import { Features } from "@/components/landing/Features";
import { FinalCta } from "@/components/landing/FinalCta";
import { SiteFooter } from "@/components/landing/SiteFooter";
import { AuthHomeRedirect } from "@/components/landing/AuthHomeRedirect";

export default function LandingPage() {
  return (
    <div className="landing min-h-screen">
      <Suspense fallback={null}>
        <AuthHomeRedirect />
      </Suspense>
      <SiteHeader />
      <main>
        <Hero />
        <Features />
        <FinalCta />
      </main>
      <SiteFooter />
    </div>
  );
}
