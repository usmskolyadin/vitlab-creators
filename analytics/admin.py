from django.contrib import admin

from .models import Blogger, SocialStats


# Register your models here.
admin.site.register(Blogger)
admin.site.register(SocialStats)