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
  video_watched: boolean;
  score: number | null;
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
