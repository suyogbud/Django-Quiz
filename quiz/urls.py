from django.urls import path

from . import views

app_name = "quiz"
urlpatterns = [
    # home page for the quiz
    path("", views.start_quiz, name="start_quiz"),
    # signup page
    path('signup/', views.signup, name='signup'),
    # quiz detail page
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # quiz results page
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # vote page
    path("<int:question_id>/vote/", views.vote, name="vote"),
    # flush page
    path("flush/", views.flush, name="flush"),
    # path("random/", views.random, name="random")
]
