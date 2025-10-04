from celery import shared_task
from .models import Blogger
from .views import update_all_platforms

@shared_task
def update_bloggers_stats():
    for b in Blogger.objects.all():
        update_all_platforms(b)
