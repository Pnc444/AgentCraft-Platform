import Link from "next/link";
import clsx from "clsx";

/**
 * Planet mark with a tilted orbit ring.
 * Paint order: back arc → planet → front arc (so the ring wraps around).
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
      <g transform="rotate(-18 24 24)">
        {/* Back half of the ring (behind the planet) */}
        <path
          d="M3 24 A21 7.5 0 0 1 45 24"
          stroke="#22D3EE"
          strokeWidth="2.5"
          strokeLinecap="round"
        />
      </g>

      {/* Planet */}
      <circle cx="24" cy="24" r="13" fill="#0b1230" stroke="#67E8F9" strokeWidth="1.5" />
      <circle cx="19" cy="19" r="4.5" fill="#1e2a5e" />

      <g transform="rotate(-18 24 24)">
        {/* Front half of the ring (in front of the planet) */}
        <path
          d="M3 24 A21 7.5 0 0 0 45 24"
          stroke="#22D3EE"
          strokeWidth="2.5"
          strokeLinecap="round"
        />
        {/* Satellite on the front arc */}
        <circle cx="42" cy="20.5" r="3" fill="#22D3EE" />
      </g>
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
      aria-label="AgentCraft"
    >
      <LogoIcon />
      {!iconOnly && (
        <span
          className={clsx(
            "text-lg font-bold tracking-tight",
            inverted ? "text-white" : "text-craft-ink"
          )}
        >
          Agent<span className="text-[#22D3EE]">Craft</span>
        </span>
      )}
    </Link>
  );
}
