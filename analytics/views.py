from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum

from services.vk_parser import get_vk_stats
from services.yt_parser import get_youtube_stats
from services.tt_parser import get_tiktok_stats
from services.ig_parser import get_instagram_stats
from .models import Blogger, SocialStats
from datetime import timedelta


def get_today_stat(blogger, platform):
    """Возвращает SocialStats за сегодня для блогера и платформы."""
    today = timezone.now().date()
    return SocialStats.objects.filter(
        blogger=blogger,
        platform=platform,
        parsed_at__date=today
    ).first()


def update_youtube_stats(blogger):
    if not blogger.youtube_url:
        return

    stat = get_today_stat(blogger, "youtube")
    
    try:
        stats = get_youtube_stats(blogger.youtube_url)
    except Exception as e:
        print(f"[YouTube] Ошибка для {blogger}: {e}")
        stats = None

    stats = stats or {"likes":0, "comments":0, "views":0, "videos":0, "subscribers":0}

    if stat:
        # обновляем существующую запись
        for key in stats:
            setattr(stat, key, stats[key])
        stat.save()
    else:
        # создаём новую
        SocialStats.objects.create(
            blogger=blogger,
            platform="youtube",
            likes=stats["likes"],
            comments=stats["comments"],
            views=stats["views"],
            videos=stats["videos"],
            subscribers=stats["subscribers"],
            parsed_at=timezone.now()
        )


def update_tiktok_stats(blogger):
    if not blogger.tiktok_url:
        return

    stat = get_today_stat(blogger, "tiktok")

    try:
        stats = get_tiktok_stats(blogger.tiktok_url)
    except Exception as e:
        print(f"[TikTok] Ошибка для {blogger}: {e}")
        stats = None

    stats = stats or {"likes":0, "comments":0, "views":0, "videos":0, "subscribers":0}

    if stat:
        for key in stats:
            setattr(stat, key, stats[key])
        stat.save()
    else:
        SocialStats.objects.create(
            blogger=blogger,
            platform="tiktok",
            likes=stats["likes"],
            comments=stats["comments"],
            views=stats["views"],
            videos=stats["videos"],
            subscribers=stats["subscribers"],
            parsed_at=timezone.now()
        )

def update_vk_stats(blogger):
    if not blogger.vk_url:
        return

    # ВСЕГДА парсим данные, без кеша
    try:
        stats = get_vk_stats(blogger.vk_url)
        print(stats)
    except Exception as e:
        print(f"[VK] Ошибка для {blogger}: {e}")
        stats = {"likes": 0, "comments": 0, "views": 0, "videos": 0, "subscribers": 0}

    stat = get_today_stat(blogger, "vk")

    if stat:
        for key, value in stats.items():
            setattr(stat, key, value)
        stat.parsed_at = timezone.now()
        stat.save()
    else:
        SocialStats.objects.create(
            blogger=blogger,
            platform="vk",
            **stats,
            parsed_at=timezone.now()
        )


def update_instagram_stats(blogger):
    if not blogger.instagram_url:
        return

    stat = get_today_stat(blogger, "instagram")

    try:
        username = blogger.instagram_url.rstrip("/").split("/")[-1]
        stats = get_instagram_stats(username)
    except Exception as e:
        print(f"[Instagram] Ошибка для {blogger}: {e}")
        stats = {"likes":0, "comments":0, "views":0, "videos":0, "subscribers":0}

    if stat:
        for key in stats:
            setattr(stat, key, stats[key])
        stat.save()
    else:
        SocialStats.objects.create(
            blogger=blogger,
            platform="instagram",
            likes=stats.get("likes",0),
            comments=stats.get("comments",0),
            views=stats.get("views",0),
            videos=stats.get("videos",0),
            subscribers=stats.get("subscribers",0),
            parsed_at=timezone.now()
        )


def update_all_platforms(blogger):
    """Обновляет все платформы для одного блогера."""
    # update_youtube_stats(blogger)
    # update_tiktok_stats(blogger)
    # update_vk_stats(blogger)
    # update_instagram_stats(blogger)

from django.db.models import Q

def bloggers_list(request):
    data = []
    platforms = ["youtube", "tiktok", "vk", "instagram"]

    name = request.GET.get("name")
    blogger_id = request.GET.get("blogger_id")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    bloggers = Blogger.objects.all()

    if name:
        bloggers = bloggers.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))

    if blogger_id:
        bloggers = bloggers.filter(id=blogger_id)

    if date_from and date_to:
        bloggers = bloggers.filter(
            stats__parsed_at__date__range=[date_from, date_to]
        ).distinct()

    for b in bloggers:
        update_all_platforms(b) 

        stats_dict = {}
        for platform in platforms:
            latest_stat = (
                SocialStats.objects.filter(blogger=b, platform=platform)
                .order_by("-parsed_at")
                .values("likes", "comments", "videos", "views", "subscribers", "parsed_at")
                .first()
            )
            if latest_stat:
                # динамически берём ссылку из Blogger по имени поля
                url_field = f"{platform}_url"
                platform_url = getattr(b, url_field, None)

                stats_dict[platform] = {
                    "likes": latest_stat["likes"],
                    "comments": latest_stat["comments"],
                    "videos": latest_stat["videos"],
                    "views": latest_stat["views"],
                    "subscribers": latest_stat["subscribers"],
                    "parsed_at": latest_stat["parsed_at"].strftime("%d.%m.%Y %H:%M"),
                    "url": platform_url,
                }

        data.append({
            "id": b.id,
            "blogger_id": b.blogger_id,
            "name": f"{b.first_name} {b.last_name}",
            "telegram_url": b.telegram_url,
            "stats": stats_dict,
        })

    print("date_from:", date_from, "date_to:", date_to)
    print("bloggers before date filter:", bloggers.count())

    return JsonResponse(data, safe=False)


def stats_summary(request):
    summary = SocialStats.objects.aggregate(
        total_likes=Sum("likes"),
        total_comments=Sum("comments"),
        total_videos=Sum("videos"),
        total_views=Sum("views"),
        total_subscribers=Sum("subscribers")
    )
    return JsonResponse(summary)


def dashboard(request):
    bloggers = Blogger.objects.prefetch_related("stats").all()
    return render(request, "index.html", {"bloggers": bloggers})

def daily(request):
    bloggers = Blogger.objects.prefetch_related("stats").all()
    return render(request, "daily.html", {"bloggers": bloggers})


from django.db.models.functions import TruncDate
from django.db.models import Max

from django.shortcuts import get_object_or_404

def blogger_history(request, blogger_id):
    try:
        blogger = Blogger.objects.get(pk=int(blogger_id))
    except (ValueError, Blogger.DoesNotExist):
        blogger = get_object_or_404(Blogger, blogger_id=blogger_id)

    stats = (
        SocialStats.objects.filter(blogger=blogger)
        .annotate(day=TruncDate("parsed_at"))
        .values("day", "platform")
        .annotate(
            likes=Max("likes"),
            comments=Max("comments"),
            videos=Max("videos"),
            views=Max("views"),
            subscribers=Max("subscribers"),
        )
        .order_by("day")
    )

    history = {}
    for row in stats:
        day = row["day"].strftime("%Y-%m-%d")
        if day not in history:
            history[day] = {}
        history[day][row["platform"]] = {
            "likes": row["likes"],
            "comments": row["comments"],
            "videos": row["videos"],
            "views": row["views"],
            "subscribers": row["subscribers"],
            "blogger_id": blogger.blogger_id,
            
        }

    daily_stats = []
    prev_day_data = None

    for day, platforms in sorted(history.items()):
        day_data = {}
        for platform, s in platforms.items():
            day_data[platform] = {
                "likes": s["likes"],
                "comments": s["comments"],
                "videos": s["videos"],
                "views": s["views"],
                "subscribers": s["subscribers"],
                "blogger_id": blogger.blogger_id,
                "name": f"{blogger.first_name} {blogger.last_name}",
            }

        if not prev_day_data:
            daily_stats.append({"day": day, "stats": day_data})
        else:
            diff = {}
            for platform, s in day_data.items():
                prev = prev_day_data.get(platform, {})
                diff[platform] = {
                    "likes": s["likes"] - prev.get("likes", 0),
                    "comments": s["comments"] - prev.get("comments", 0),
                    "videos": s["videos"] - prev.get("videos", 0),
                    "views": s["views"] - prev.get("views", 0),
                    "subscribers": s["subscribers"] - prev.get("subscribers", 0),
                    "name": s["name"],  # имя блогера тут тоже
                }
            daily_stats.append({"day": day, "stats": diff})

        prev_day_data = day_data


    return JsonResponse(daily_stats, safe=False)

from django.db.models import Max
from django.db.models.functions import TruncDate
from django.http import JsonResponse

from django.db.models.functions import TruncDate
from django.http import JsonResponse
def all_bloggers_history(request):
    # Получаем все SocialStats, группируем по дню и блогеру
    stats = (
        SocialStats.objects
        .select_related("blogger")
        .annotate(day=TruncDate("parsed_at"))
        .values("day", "blogger__id", "blogger__first_name", "blogger__last_name", "platform")
        .annotate(
            likes=Max("likes"),
            comments=Max("comments"),
            videos=Max("videos"),
            views=Max("views"),
            subscribers=Max("subscribers"),
        )
        .order_by("day", "blogger__id", "platform")
    )

    # Словарь для объединения платформ по дню и блогеру
    history_dict = {}

    for row in stats:
        key = (row["day"], row["blogger__id"])

        if key not in history_dict:
            history_dict[key] = {
                "day": row["day"].strftime("%Y-%m-%d"),
                "blogger_id": row["blogger__id"],
                "name": f'{row["blogger__first_name"]} {row["blogger__last_name"]}',
                "stats": {}
            }

        # Сохраняем статистику по платформе
        history_dict[key]["stats"][row["platform"]] = {
            "likes": row["likes"],
            "comments": row["comments"],
            "videos": row["videos"],
            "views": row["views"],
            "subscribers": row["subscribers"],
        }

    # Список для финального JSON с подсчетом дельты относительно предыдущего дня
    final_history = []
    prev_day_data = {}

    for key in sorted(history_dict.keys()):
        day_record = history_dict[key]
        day = day_record["day"]
        blogger_id = day_record["blogger_id"]
        stats_today = day_record["stats"]

        # Вычисляем дельту по сравнению с предыдущим днем для этого блогера
        delta_stats = {}
        prev_stats = prev_day_data.get(blogger_id, {})
        for platform, s in stats_today.items():
            prev = prev_stats.get(platform, {})
            delta_stats[platform] = {
                "likes": s["likes"] - prev.get("likes", 0),
                "comments": s["comments"] - prev.get("comments", 0),
                "videos": s["videos"] - prev.get("videos", 0),
                "views": s["views"] - prev.get("views", 0),
                "subscribers": s["subscribers"] - prev.get("subscribers", 0),
            }

        final_history.append({
            "day": day,
            "blogger_id": blogger_id,
            "name": day_record["name"],
            "stats": delta_stats
        })

        prev_day_data[blogger_id] = stats_today

    return JsonResponse(final_history, safe=False)