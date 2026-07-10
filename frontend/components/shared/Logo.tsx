import Link from "next/link";
import clsx from "clsx";

/**
 * AgentCraft logo — planet with an orbit ring, plus optional wordmark.
 * Inline SVG so it scales crisply and adapts to the dark theme.
 */
export function LogoIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 48 48"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={clsx("h-8 w-8", className)}
      aria-hidden
    >
      {/* planet */}
      <circle cx="24" cy="24" r="13" fill="#0b1230" stroke="#a5b4fc" strokeWidth="1.5" />
      {/* highlight */}
      <circle cx="19" cy="19" r="4.5" fill="#1e2a5e" />
      {/* orbit ring (tilted ellipse) */}
      <ellipse
        cx="24"
        cy="24"
        rx="21"
        ry="7.5"
        stroke="#3b82f6"
        strokeWidth="2.5"
        transform="rotate(-18 24 24)"
      />
      {/* satellite dot on the ring */}
      <circle cx="42.5" cy="17" r="3" fill="#3b82f6" />
    </svg>
  );
}

interface LogoProps {
  /** Where the logo links to. Defaults to "/". */
  href?: string;
  /** Hide the "AgentCraft" text and show only the planet icon. */
  iconOnly?: boolean;
  className?: string;
}

export function Logo({ href = "/", iconOnly = false, className }: LogoProps) {
  return (
    <Link
      href={href}
      className={clsx("flex items-center gap-2.5", className)}
      aria-label="AgentCraft"
    >
      <LogoIcon />
      {!iconOnly && (
        <span className="text-lg font-bold tracking-tight text-white">
          Agent<span className="text-blue-500">Craft</span>
        </span>
      )}
    </Link>
  );
}
