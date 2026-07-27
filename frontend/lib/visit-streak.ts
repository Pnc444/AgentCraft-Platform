const STREAK_KEY = "agentcraft-visit-streak";

type StreakState = {
  lastDay: string; // YYYY-MM-DD local
  count: number;
};

function todayKey() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function yesterdayKey() {
  const d = new Date();
  d.setDate(d.getDate() - 1);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

/** Client-only consecutive calendar-day visit streak. Honest local metric. */
export function recordAndGetVisitStreak(): number {
  if (typeof window === "undefined") return 0;
  try {
    const today = todayKey();
    const raw = localStorage.getItem(STREAK_KEY);
    const prev = raw ? (JSON.parse(raw) as StreakState) : null;

    let count = 1;
    if (prev?.lastDay === today) {
      count = Math.max(1, prev.count || 1);
    } else if (prev?.lastDay === yesterdayKey()) {
      count = Math.max(1, (prev.count || 0) + 1);
    }

    localStorage.setItem(STREAK_KEY, JSON.stringify({ lastDay: today, count }));
    return count;
  } catch {
    return 1;
  }
}

export function peekVisitStreak(): number {
  if (typeof window === "undefined") return 0;
  try {
    const raw = localStorage.getItem(STREAK_KEY);
    if (!raw) return 0;
    const prev = JSON.parse(raw) as StreakState;
    if (prev.lastDay === todayKey() || prev.lastDay === yesterdayKey()) {
      return Math.max(0, prev.count || 0);
    }
    return 0;
  } catch {
    return 0;
  }
}
