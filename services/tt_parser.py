import requests
import re
import json
from typing import Optional


def get_tiktok_stats(profile_url: str) -> Optional[dict]:
    """
    Парсит публичный TikTok-профиль по ссылке и достает:
    - подписчики
    - лайки
    - количество видео
    - просмотры (сумма по роликам)
    - количество комментариев (сумма по роликам)
    - url аватарки
    """

    try:
        username = profile_url.rstrip("/").split("/")[-1].replace("@", "")
        url = f"https://www.tiktok.com/@{username}"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9"
        }

        res = requests.get(url, headers=headers)
        res.raise_for_status()
        html = res.text

        # 1. Пробуем SIGI_STATE (основной JSON TikTok)
        match = re.search(r'<script id="SIGI_STATE" type="application/json">(.*?)</script>', html)
        if match:
            data = json.loads(match.group(1))
        else:
            # 2. Пробуем новый формат (__UNIVERSAL_DATA_FOR_REHYDRATION__)
            match = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>', html)
            if not match:
                print("❌ Не удалось найти JSON в HTML")
                return None
            raw_json = match.group(1)
            data = json.loads(raw_json)

            props = data.get("__DEFAULT_SCOPE__", {}).get("webapp.user-detail", {}).get("userInfo", {})
            if props:
                user_data = props.get("user", {})
                stats_data = props.get("stats", {})

                avatar_url = user_data.get("avatarLarger", "")
                print(f"🖼 URL аватарки: {avatar_url}")

                stats = {
                    "subscribers": stats_data.get("followerCount", 0),
                    "likes": stats_data.get("heart", 0),
                    "videos": stats_data.get("videoCount", 0),
                    "views": 0,
                    "comments": 0,
                    "avatar_url": avatar_url
                }
                return stats

        # ========== Старый формат SIGI_STATE ==========
        user_data = list(data["UserModule"]["users"].values())[0]
        stats_data = list(data["UserModule"]["stats"].values())[0]

        avatar_url = user_data.get("avatarLarger", "")
        print(f"🖼 URL аватарки: {avatar_url}")

        stats = {
            "subscribers": stats_data.get("followerCount", 0),
            "likes": stats_data.get("heart", 0),
            "videos": stats_data.get("videoCount", 0),
            "views": 0,
            "comments": 0,
            "avatar_url": avatar_url
        }

        # Если есть данные по видео — считаем просмотры и комментарии
        if "ItemModule" in data:
            for video in data["ItemModule"].values():
                stats["views"] += video.get("stats", {}).get("playCount", 0)
                stats["comments"] += video.get("stats", {}).get("commentCount", 0)

        return stats

    except Exception as e:
        print(f"Ошибка TikTok: {e}")
        return None


if __name__ == "__main__":
    profile = "https://www.tiktok.com/@charlidamelio"
    result = get_tiktok_stats(profile)
    print(json.dumps(result, indent=2, ensure_ascii=False))
