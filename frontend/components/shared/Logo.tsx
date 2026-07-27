import Link from "next/link";
import clsx from "clsx";

/** Purple shield mark with a K monogram. */
export function LogoIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 48 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={clsx("h-8 w-8", className)}
      aria-hidden
    >
      <path
        d="M24 4L40 10.5V22.5C40 32.2 33.2 40.6 24 43.5C14.8 40.6 8 32.2 8 22.5V10.5L24 4Z"
        fill="#7C3AED"
      />
      <path
        d="M24 7.2L36.5 12.2V22.5C36.5 30.4 31.1 37.4 24 40C16.9 37.4 11.5 30.4 11.5 22.5V12.2L24 7.2Z"
        fill="#8B5CF6"
      />
      <text
        x="24"
        y="26.5"
        textAnchor="middle"
        dominantBaseline="middle"
        fill="white"
        fontSize="16"
        fontWeight="800"
        fontFamily="ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
      >
        K
      </text>
    </svg>
  );
}

interface LogoProps {
  href?: string;
  iconOnly?: boolean;
  className?: string;
  inverted?: boolean;
}

export function Logo({ href = "/", iconOnly = false, className, inverted = false }: LogoProps) {
  return (
    <Link
      href={href}
      className={clsx("flex items-center gap-2.5", className)}
      aria-label="Knight's Academy"
    >
      <LogoIcon />
      {!iconOnly && (
        <span
          className={clsx(
            "text-lg font-bold tracking-tight",
            inverted ? "text-[#F8FAFC]" : "text-craft-ink"
          )}
        >
          Knight&apos;s{" "}
          <span className={inverted ? "text-[#C4B5FD]" : "text-violet-600 dark:text-violet-400"}>
            Academy
          </span>
        </span>
      )}
    </Link>
  );
}
