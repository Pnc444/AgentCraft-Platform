"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useMemo } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Award, BookOpen, LayoutDashboard, Settings } from "lucide-react";
import clsx from "clsx";
import { getCourses } from "@/lib/api/courses";
import { currentModule, trackModulesFrom } from "@/lib/learning-track";

const tabs = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard, match: (p: string) => p === "/dashboard" },
  { href: "lessons", label: "Lessons", icon: BookOpen, match: (p: string) => p.includes("/courses/") },
  {
    href: "/dashboard/certificates",
    label: "Certificates",
    icon: Award,
    match: (p: string) => p.startsWith("/dashboard/certificates"),
  },
  {
    href: "/dashboard/profile",
    label: "Settings",
    icon: Settings,
    match: (p: string) => p.startsWith("/dashboard/profile") || p.startsWith("/dashboard/settings"),
  },
] as const;

/** Thumb-zone primary nav for phones. Hidden on lg+. */
export function MobileBottomNav() {
  const pathname = usePathname();
  const queryClient = useQueryClient();
  const { data: courses } = useQuery({
    queryKey: ["courses"],
    queryFn: async () => {
      const list = await getCourses();
      for (const course of list) {
        queryClient.setQueryData(["course", course.slug], course);
      }
      return list;
    },
  });

  const lessonsHref = useMemo(() => {
    const track = trackModulesFrom(courses ?? []);
    const target = currentModule(track) ?? track[0];
    if (target) return `/dashboard/courses/${target.slug}`;
    if (!courses?.length) return "/dashboard";
    return `/dashboard/courses/${courses[0].slug}`;
  }, [courses]);

  // Hide on immersive lesson routes? Keep visible for orientation — mockup mobile uses bottom tabs on dashboard; lesson has its own chrome. Hide when in a lesson to free space.
  const inLesson = /\/lessons\/[^/]+\//.test(pathname);
  if (inLesson) return null;

  return (
    <nav
      className="fixed inset-x-0 bottom-0 z-30 border-t border-craft-border bg-craft-surface/95 pb-[env(safe-area-inset-bottom)] backdrop-blur-md lg:hidden"
      aria-label="Primary"
    >
      <ul className="grid grid-cols-4 gap-1 px-2 py-1.5">
        {tabs.map((tab) => {
          const href = tab.href === "lessons" ? lessonsHref : tab.href;
          const active = tab.match(pathname);
          const Icon = tab.icon;
          return (
            <li key={tab.label}>
              <Link
                href={href}
                className={clsx(
                  "flex min-h-[48px] flex-col items-center justify-center gap-0.5 rounded-xl text-[11px] font-medium transition",
                  active
                    ? "bg-violet-600 text-white shadow-btn"
                    : "text-craft-faint hover:text-craft-muted"
                )}
              >
                <Icon className="h-5 w-5" />
                {tab.label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
