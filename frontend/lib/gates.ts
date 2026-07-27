import { useAuthStore } from "@/stores/authStore";

/**
 * Whether the signed-in account skips the course's progression gates.
 *
 * The course locks itself as a learner moves through it: a module stays shut
 * until the one before it is finished, and an assessment stays shut until the
 * lesson video has been played to the end. That is right for students and
 * miserable for anyone reviewing or authoring content, who would otherwise
 * have to play the whole course through to look at Module 7.
 *
 * Staff are exempt. `is_staff` is Django's own flag, so `createsuperuser` and
 * the `create_admin` command both grant it, and the API serves it **read-only**
 * — `/api/v1/auth/me/` accepts PATCH, so a writable flag would let any student
 * hand themselves the bypass.
 *
 * This is a convenience for people who already hold the keys, not a security
 * boundary. The gates were only ever enforced in the browser: the lesson and
 * quiz endpoints never checked progression, so anyone willing to type a URL
 * could always reach any lesson. Nothing here widens that. If gating ever needs
 * to be real, it has to be enforced server-side, and this flag would then be
 * the thing the server checks.
 */
export function useCanBypassGates(): boolean {
  return useAuthStore((s) => !!s.user?.is_staff);
}
