import Link from "next/link";

/**
 * Framework-level 404. Next's default is a bare "This page could not be found."
 * with no links — a dead end, the same defect the course/lesson not-found
 * states were fixed for (audit F2, acceptance check #16: every error state
 * offers at least one action that moves the learner somewhere real).
 */
export default function NotFound() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-craft-canvas px-6">
      <div className="max-w-md text-center">
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-craft-faint">404</p>
        <h1 className="mt-2 text-2xl font-bold text-craft-ink">That page doesn&apos;t exist.</h1>
        <p className="mt-2 text-sm text-craft-muted">
          The link may be out of date. Your courses are waiting on the dashboard.
        </p>
        <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
          <Link href="/dashboard" className="btn-primary">
            Back to my courses
          </Link>
          <Link href="/" className="btn-secondary">
            Go to the homepage
          </Link>
        </div>
      </div>
    </main>
  );
}
