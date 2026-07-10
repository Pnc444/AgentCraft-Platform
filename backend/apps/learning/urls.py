from django.urls import path

from .views import DashboardStatsView, LessonProgressView, RecommendationListView

urlpatterns = [
    path("lessons/<int:lesson_id>/progress/", LessonProgressView.as_view(), name="lesson-progress"),
    path("recommendations/", RecommendationListView.as_view(), name="recommendation-list"),
    path("dashboard/stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
]
