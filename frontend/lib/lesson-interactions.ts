import type { LessonInteraction } from "@/types";

export function findInteraction(
  interactionLog: LessonInteraction[] | undefined,
  key: string
) {
  return (interactionLog || []).find((entry) => entry.key === key);
}

export function interactionDone(
  interactionLog: LessonInteraction[] | undefined,
  key: string,
  expectedStatus = "done"
) {
  const entry = findInteraction(interactionLog, key);
  return entry?.status === expectedStatus;
}

export function completedCheckpointIds(interactionLog: LessonInteraction[] | undefined) {
  return new Set(
    (interactionLog || [])
      .filter((entry) => entry.type === "checkpoint" && entry.status === "passed")
      .map((entry) => entry.key)
  );
}

export function completedInteractionKeys(
  interactionLog: LessonInteraction[] | undefined,
  type: string,
  status = "done"
) {
  return new Set(
    (interactionLog || [])
      .filter((entry) => entry.type === type && entry.status === status)
      .map((entry) => entry.key)
  );
}