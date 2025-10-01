from django.urls import path
from . import views

urlpatterns = [
    path("api/bloggers/", views.bloggers_list, name="bloggers_list"),
    path("bloggers_list/", views.bloggers_list),
    path("api/summary/", views.stats_summary, name="stats_summary"),
    path("blogger_history/<int:blogger_id>/", views.blogger_history, name="blogger_history"),
    path("all_bloggers_history/", views.all_bloggers_history, name="all_bloggers_history"),
    path("", views.dashboard, name="dashboard"),
    path("daily", views.daily, name="daily"),
]