from django.urls import path

from .views import TutorAskView, TutorSuggestionsView

urlpatterns = [
    path("tutor/ask/", TutorAskView.as_view(), name="tutor-ask"),
    path("tutor/suggestions/", TutorSuggestionsView.as_view(), name="tutor-suggestions"),
]
