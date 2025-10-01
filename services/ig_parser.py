from apify_client import ApifyClient
from django.utils import timezone
from django.core.cache import cache 

API_KEY = ""
CACHE_TTL = 600 


def get_instagram_stats(username: str) -> dict:
    cache_key = f"instagram_stats:{username}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    client = ApifyClient(API_KEY)

    try:
        run = client.actor("apify/instagram-scraper").call(run_input={
            "directUrls": [f"https://www.instagram.com/{username}/"],
            "resultsLimit": 50
        })

        dataset_id = run["defaultDatasetId"]
        items = list(client.dataset(dataset_id).iterate_items())

        if not items:
            stats = {"likes": 0, "comments": 0, "videos": 0, "views": 0, "subscribers": 0}
            cache.set(cache_key, stats, CACHE_TTL)
            return stats

        stats = {
            "likes": 0,
            "comments": 0,
            "videos": 0,
            "views": 0,
            "subscribers": 0
        }

        for post in items:
            stats["likes"] += post.get("likesCount", 0)
            stats["comments"] += post.get("commentsCount", 0)
            if post.get("type") == "Video":
                stats["videos"] += 1
                stats["views"] += post.get("videoViewCount", 0)

        stats["subscribers"] = items[0].get("ownerFollowersCount", 0)

        print(stats)
        cache.set(cache_key, stats, CACHE_TTL)

        return stats

    except Exception as e:
        print(f"Ошибка получения инсты {username}: {e}")
        return {"likes": 0, "comments": 0, "videos": 0, "views": 0, "subscribers": 0}