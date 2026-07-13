import { apiClient } from "./client";
import type {
  CourseDetail,
  DashboardStats,
  LessonDetail,
  LessonStatus,
  Recommendation,
} from "@/types";

/** Courses with nested lesson summaries + progress (single request). */
export function getCourses(): Promise<CourseDetail[]> {
  return apiClient<CourseDetail[]>("/courses/");
}

export function getCourse(slug: string): Promise<CourseDetail> {
  return apiClient<CourseDetail>(`/courses/${slug}/`);
}

export function getLesson(courseSlug: string, lessonSlug: string): Promise<LessonDetail> {
  return apiClient<LessonDetail>(`/courses/${courseSlug}/lessons/${lessonSlug}/`);
}

export function updateLessonProgress(
  lessonId: number,
  data: {
    status?: LessonStatus;
    score?: number;
    video_watched?: boolean;
  }
): Promise<{
  lesson_id: number;
  status: LessonStatus;
  score: number | null;
  video_watched: boolean;
}> {
  return apiClient(`/lessons/${lessonId}/progress/`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function getRecommendations(): Promise<Recommendation[]> {
  return apiClient<Recommendation[]>("/recommendations/");
}

export function getDashboardStats(): Promise<DashboardStats> {
  return apiClient<DashboardStats>("/dashboard/stats/");
}
