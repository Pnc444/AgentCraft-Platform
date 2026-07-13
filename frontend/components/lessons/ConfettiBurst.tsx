"use client";

import { useEffect, useRef } from "react";

type Particle = {
  x: number;
  y: number;
  vx: number;
  vy: number;
  rotation: number;
  spin: number;
  color: string;
  w: number;
  h: number;
  life: number;
};

const COLORS = ["#22D3EE", "#06B6D4", "#34D399", "#FBBF24", "#F472B6", "#A5F3FC", "#67E8F9"];

/** Lightweight canvas confetti — no dependency. */
export function ConfettiBurst({ active, durationMs = 2800 }: { active: boolean; durationMs?: number }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!active) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let raf = 0;
    let running = true;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    function resize() {
      const { innerWidth: w, innerHeight: h } = window;
      canvas!.width = w * dpr;
      canvas!.height = h * dpr;
      canvas!.style.width = `${w}px`;
      canvas!.style.height = `${h}px`;
      ctx!.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resize();
    window.addEventListener("resize", resize);

    const particles: Particle[] = [];
    const originX = window.innerWidth / 2;
    const originY = window.innerHeight * 0.35;

    for (let i = 0; i < 140; i++) {
      const angle = (Math.PI * 2 * i) / 140 + (Math.random() - 0.5) * 0.4;
      const speed = 6 + Math.random() * 10;
      particles.push({
        x: originX + (Math.random() - 0.5) * 40,
        y: originY + (Math.random() - 0.5) * 20,
        vx: Math.cos(angle) * speed * (0.4 + Math.random()),
        vy: Math.sin(angle) * speed * 0.35 - (8 + Math.random() * 8),
        rotation: Math.random() * 360,
        spin: (Math.random() - 0.5) * 18,
        color: COLORS[i % COLORS.length],
        w: 6 + Math.random() * 6,
        h: 8 + Math.random() * 10,
        life: 1,
      });
    }

    // Second burst from the sides
    for (let i = 0; i < 60; i++) {
      const fromLeft = i % 2 === 0;
      particles.push({
        x: fromLeft ? 0 : window.innerWidth,
        y: window.innerHeight * (0.25 + Math.random() * 0.35),
        vx: (fromLeft ? 1 : -1) * (8 + Math.random() * 10),
        vy: -4 - Math.random() * 8,
        rotation: Math.random() * 360,
        spin: (Math.random() - 0.5) * 16,
        color: COLORS[i % COLORS.length],
        w: 5 + Math.random() * 5,
        h: 7 + Math.random() * 8,
        life: 1,
      });
    }

    const started = performance.now();
    const gravity = 0.22;
    const drag = 0.992;

    function frame(now: number) {
      if (!running || !ctx || !canvas) return;
      const elapsed = now - started;
      const fade = Math.max(0, 1 - elapsed / durationMs);
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (const p of particles) {
        p.vx *= drag;
        p.vy = p.vy * drag + gravity;
        p.x += p.vx;
        p.y += p.vy;
        p.rotation += p.spin;
        p.life = fade;

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate((p.rotation * Math.PI) / 180);
        ctx.globalAlpha = Math.min(1, p.life * 1.2);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
        ctx.restore();
      }

      if (elapsed < durationMs) {
        raf = requestAnimationFrame(frame);
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    }

    raf = requestAnimationFrame(frame);

    return () => {
      running = false;
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
    };
  }, [active, durationMs]);

  if (!active) return null;

  return (
    <canvas
      ref={canvasRef}
      className="pointer-events-none fixed inset-0 z-[90]"
      aria-hidden
    />
  );
}
