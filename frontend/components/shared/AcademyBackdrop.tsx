import clsx from "clsx";

interface AcademyBackdropProps {
  className?: string;
  /** Softer grid for dense app pages */
  subtle?: boolean;
}

/** Soft animated grid + cyan glow used on the hero and dashboard. */
export function AcademyBackdrop({ className, subtle = false }: AcademyBackdropProps) {
  return (
    <div className={clsx("pointer-events-none absolute inset-0 overflow-hidden", className)} aria-hidden>
      <div
        className={clsx(
          "absolute inset-[-48px] academy-grid",
          subtle ? "opacity-[0.35]" : "opacity-[0.45]"
        )}
        style={{
          backgroundImage:
            "linear-gradient(to right, #e2e8f0 1px, transparent 1px), linear-gradient(to bottom, #e2e8f0 1px, transparent 1px)",
          backgroundSize: "48px 48px",
          maskImage: subtle
            ? "radial-gradient(ellipse at 50% 0%, black 10%, transparent 70%)"
            : "radial-gradient(ellipse at center, black 20%, transparent 75%)",
          WebkitMaskImage: subtle
            ? "radial-gradient(ellipse at 50% 0%, black 10%, transparent 70%)"
            : "radial-gradient(ellipse at center, black 20%, transparent 75%)",
        }}
      />
      <div
        className={clsx(
          "academy-glow absolute rounded-full bg-cyan-200/40 blur-3xl",
          subtle
            ? "right-[-4rem] top-0 h-[22rem] w-[22rem]"
            : "right-0 top-24 h-[28rem] w-[28rem]"
        )}
      />
    </div>
  );
}
