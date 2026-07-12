import { SiteHeader } from "@/components/landing/SiteHeader";
import { SiteFooter } from "@/components/landing/SiteFooter";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="landing flex min-h-screen flex-col bg-[#F8FAFC]">
      <SiteHeader />
      <main className="flex flex-1 items-center justify-center px-6 pb-12 pt-28">{children}</main>
      <SiteFooter />
    </div>
  );
}
