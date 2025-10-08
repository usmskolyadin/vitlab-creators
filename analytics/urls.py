from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("api/bloggers/", views.bloggers_list, name="bloggers_list"),
    path("bloggers_list/", views.bloggers_list),
    path("api/summary/", views.stats_summary, name="stats_summary"),
    path("blogger_history/<int:blogger_id>/", views.blogger_history, name="blogger_history"),
    path("all_bloggers_history/", views.all_bloggers_history, name="all_bloggers_history"),
    path("", views.dashboard, name="dashboard"),
    path("daily", views.daily, name="daily"),

    # выходим на /
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # стандартная админка
    path('admin/', admin.site.urls),
]
