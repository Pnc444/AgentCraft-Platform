"use client";

import Link from "next/link";
import { useParams, usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { BookOpen, ChevronDown, LayoutDashboard, LogOut } from "lucide-react";
import clsx from "clsx";
import { getCourses, getDashboardStats } from "@/lib/api/courses";
import { useAuthStore } from "@/stores/authStore";

interface SidebarProps {
  mobileOpen: boolean;
  onMobileClose: () => void;
}

export function Sidebar({ mobileOpen, onMobileClose }: SidebarProps) {
  const pathname = usePathname();
  const params = useParams();
  const router = useRouter();
  const logout = useAuthStore((s) => s.logout);
  const [coursesOpen, setCoursesOpen] = useState(pathname.includes("/courses/"));

  const { data: courses } = useQuery({ queryKey: ["courses"], queryFn: getCourses });
  const { data: stats } = useQuery({ queryKey: ["dashboard-stats"], queryFn: getDashboardStats });

  function handleLogout() {
    logout();
    router.push("/login");
  }

  return (
    <aside
      className={clsx(
        "fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-white/5 bg-craft-900 transition-transform lg:static lg:translate-x-0",
        mobileOpen ? "translate-x-0" : "-translate-x-full"
      )}
      aria-label="Main navigation"
    >
      <div className="flex h-16 items-center px-5">
        <Link href="/dashboard" className="flex items-center gap-2 text-lg font-bold text-white" onClick={onMobileClose}>
          <span aria-hidden>⚡</span>
          Agent<span className="text-craft-accent">Craft</span>
        </Link>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-2">
        <Link
          href="/dashboard"
          onClick={onMobileClose}
          className={clsx(
            "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors",
            pathname === "/dashboard"
              ? "bg-craft-accent/15 text-white"
              : "text-slate-400 hover:bg-white/5 hover:text-white"
          )}
        >
          <LayoutDashboard className="h-4 w-4" />
          Dashboard
        </Link>

        <button
          type="button"
          onClick={() => setCoursesOpen((v) => !v)}
          className={clsx(
            "flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-colors",
            pathname.includes("/courses/")
              ? "bg-craft-accent/15 text-white"
              : "text-slate-400 hover:bg-white/5 hover:text-white"
          )}
          aria-expanded={coursesOpen}
        >
          <BookOpen className="h-4 w-4" />
          Courses
          <ChevronDown className={clsx("ml-auto h-4 w-4 transition-transform", coursesOpen && "rotate-180")} />
        </button>

        {coursesOpen && (
          <div className="ml-4 space-y-1 border-l border-white/10 pl-3">
            <p className="px-2 pt-2 text-xs uppercase tracking-wide text-slate-600">Your courses</p>
            {courses?.map((course) => (
              <Link
                key={course.slug}
                href={`/dashboard/courses/${course.slug}`}
                onClick={onMobileClose}
                className={clsx(
                  "block rounded-lg px-2 py-2 text-sm transition-colors",
                  params.slug === course.slug
                    ? "bg-craft-accent/15 text-white"
                    : "text-slate-400 hover:bg-white/5 hover:text-white"
                )}
              >
                <span className="block truncate">{course.title}</span>
                <span className="text-xs text-slate-600">{course.total_lessons} lessons</span>
              </Link>
            ))}
            {courses?.length === 0 && <p className="px-2 py-2 text-sm text-slate-600">No courses yet.</p>}
          </div>
        )}
      </nav>

      <div className="border-t border-white/5 px-5 py-4">
        <p className="text-xs uppercase tracking-wide text-slate-600">Learning path</p>
        <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-craft-800">
          <div
            className="h-full rounded-full bg-gradient-to-r from-craft-accent to-craft-glow transition-all"
            style={{ width: `${stats?.overall_progress_pct ?? 0}%` }}
          />
        </div>
        <p className="mt-2 text-xs text-slate-500">Keep going — one lesson at a time.</p>
      </div>

      <div className="border-t border-white/5 p-3">
        <button
          type="button"
          onClick={handleLogout}
          className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-slate-400 transition-colors hover:bg-white/5 hover:text-white"
        >
          <LogOut className="h-4 w-4" />
          Log out
        </button>
      </div>
    </aside>
  );
}
