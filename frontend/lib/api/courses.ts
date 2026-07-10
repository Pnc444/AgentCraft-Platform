import { apiClient } from "./client";
import type {
  Course,
  CourseDetail,
  DashboardStats,
  LessonDetail,
  LessonStatus,
  Recommendation,
} from "@/types";

export function getCourses(): Promise<Course[]> {
  return apiClient<Course[]>("/courses/");
}

export function getCourse(slug: string): Promise<CourseDetail> {
  return apiClient<CourseDetail>(`/courses/${slug}/`);
}

export function getLesson(courseSlug: string, lessonSlug: string): Promise<LessonDetail> {
  return apiClient<LessonDetail>(`/courses/${courseSlug}/lessons/${lessonSlug}/`);
}

export function updateLessonProgress(
  lessonId: number,
  status: LessonStatus
): Promise<{ lesson_id: number; status: LessonStatus }> {
  return apiClient(`/lessons/${lessonId}/progress/`, {
    method: "POST",
    body: JSON.stringify({ status }),
  });
}

export function getRecommendations(): Promise<Recommendation[]> {
  return apiClient<Recommendation[]>("/recommendations/");
}

export function getDashboardStats(): Promise<DashboardStats> {
  return apiClient<DashboardStats>("/dashboard/stats/");
}
