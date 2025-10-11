from django.db import models


class Blogger(models.Model):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)

    blogger_id = models.CharField("Creator №", max_length=255)
    
    telegram_url = models.CharField("Ссылка телеграм", max_length=255, default="https://t.me/")
    
    vk_url = models.URLField("VK профиль", blank=True, null=True)
    instagram_url = models.URLField("Instagram профиль", blank=True, null=True)
    youtube_url = models.URLField("YouTube профиль", blank=True, null=True)
    tiktok_url = models.URLField("TikTok профиль", blank=True, null=True)

    avatar_url = models.CharField("URL Аватарки", max_length=2500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SocialStats(models.Model):
    PLATFORM_CHOICES = [
        ("vk", "VK"),
        ("instagram", "Instagram"),
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
    ]


    blogger = models.ForeignKey(
        Blogger,
        on_delete=models.CASCADE,
        related_name="stats"
    )

    platform = models.CharField("Соцсеть", max_length=20, choices=PLATFORM_CHOICES)

    likes = models.PositiveIntegerField("Лайки", default=0)
    comments = models.PositiveIntegerField("Комментарии", default=0)
    videos = models.PositiveIntegerField("Видео", default=0)
    views = models.PositiveBigIntegerField("Просмотры", default=0)
    subscribers = models.IntegerField(default=0)
    
    parsed_at = models.DateTimeField("Дата парсинга", auto_now_add=True)

    class Meta:
        ordering = ["-parsed_at"]  

    def __str__(self):
        return f"{self.blogger} [{self.get_platform_display()}] {self.parsed_at.strftime('%d.%m.%Y %H:%M')}"
