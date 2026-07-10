import type { Metadata } from "next";
import { QueryProvider } from "@/components/shared/QueryProvider";
import "./globals.css";

export const metadata: Metadata = {
  title: "AgentCraft — Learn AI agents from zero",
  description:
    "AgentCraft helps students progress from beginner concepts to real AI agent projects through guided lessons, hands-on practice, and a structured learning roadmap.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
