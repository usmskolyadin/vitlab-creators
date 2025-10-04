import django
import os
from django.utils import timezone
from django.core.cache import cache
from .models import Blogger
from .views import update_all_platforms

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

print(f"[{timezone.now()}] Updating bloggers stats...")
for blogger in Blogger.objects.all():
    update_all_platforms(blogger)
    
cache.clear()
print("All bloggers updated and cache cleared.")
