import type { CheckpointQuestion } from "@/components/lessons/CheckpointQuiz";

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: "student" | "ai_instructor";
  skill_profile: Record<string, number>;
  avatar: string | null;
}

export type LessonStatus = "not_started" | "in_progress" | "completed" | "stuck";

export type LessonType = "theory" | "interactive" | "sandbox" | "quiz" | "agent_lab";

export interface GuidedLessonBlock {
  title: string;
  body: string;
  analogy?: string;
  try_this?: string[];
  remember?: string;
  checkpoint_after?: boolean;
  checkpoint_questions?: CheckpointQuestion[];
  kind?: "common_mistake" | "teach_it_back";
  artifact_paths?: string[];
  interactive_widget?: "capstone_studio" | "openclaw_file_explorer";
  /** Brilliant-style: question shown BEFORE the explanation to prompt thinking first. */
  predict_first?: { question: string; hint?: string };
}

export interface LessonInteraction {
  type: string;
  key: string;
  status?: string;
  timestamp?: string;
  details?: Record<string, unknown>;
}

export interface CapstoneAssignmentSection {
  key: string;
  label: string;
  prompt: string;
  placeholder?: string;
  min_length?: number;
  required_keywords?: string[];
}

export interface CapstoneAssignment {
  title: string;
  summary: string;
  sections: CapstoneAssignmentSection[];
  review_questions: string[];
  risky_phrases?: string[];
}

export interface LessonArtifact {
  path: string;
  summary: string;
  format?: "text" | "json";
  inspect_prompt?: string;
  change_prompt?: string;
  body?: string | Record<string, unknown> | unknown[];
}

export interface Skill {
  id: number;
  name: string;
  slug: string;
  description: string;
  order: number;
}

export interface LessonSummary {
  id: number;
  title: string;
  slug: string;
  lesson_type: LessonType;
  order: number;
  estimated_minutes: number;
  status: LessonStatus;
}

export interface LessonDetail extends LessonSummary {
  content: string;
  video_url: string;
  require_full_watch: boolean;
  video_watched: boolean;
  score: number | null;
  interaction_log: LessonInteraction[];
  sandbox_config: Record<string, unknown>;
  course_slug: string;
  course_title: string;
}

export interface Course {
  id: number;
  title: string;
  slug: string;
  description: string;
  skill: Skill;
  order: number;
  difficulty: 1 | 2 | 3;
  total_lessons: number;
  completed_lessons: number;
  total_minutes: number | null;
  completion_pct: number;
}

export interface CourseDetail extends Course {
  lessons: LessonSummary[];
}

export interface Recommendation {
  id: number;
  reason: string;
  confidence: number;
  is_read: boolean;
  lesson_title: string;
  lesson_slug: string;
  course_title: string;
  course_slug: string;
}

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlocked: boolean;
  equipped: boolean;
}

export interface DashboardStats {
  lessons_completed: number;
  lessons_in_progress: number;
  total_lessons: number;
  overall_progress_pct: number;
  badges: Badge[];
  badges_unlocked: number;
  badges_total: number;
}
