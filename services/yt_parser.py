import yt_dlp

YOUTUBE_API_KEY=""

def get_youtube_stats(channel_url: str):
    from googleapiclient.discovery import build
    print(1)
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # Получаем channel_id
    if "channel/" in channel_url:
        channel_id = channel_url.split("channel/")[1].split("/")[0]
    else:
        username = channel_url.rstrip("/").split("/")[-1].replace("@", "")
        res = youtube.search().list(
            part="snippet",
            q=username,
            type="channel",
            maxResults=1
        ).execute()
        items = res.get("items", [])
        if not items:
            raise ValueError(f"Не удалось получить channel_id для {channel_url}")
        channel_id = items[0]["snippet"]["channelId"]

    # Данные канала
    channel_res = youtube.channels().list(
        part="statistics,contentDetails",
        id=channel_id
    ).execute()

    if not channel_res['items']:
        raise ValueError(f"Канал {channel_url} не найден")

    stats = channel_res['items'][0]['statistics']
    uploads_playlist = channel_res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    total_subscribers = int(stats.get("subscriberCount", 0))

    # Получаем видео
    video_ids = []
    next_page = None
    while True:
        pl_res = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist,
            maxResults=50,
            pageToken=next_page
        ).execute()
        video_ids += [v['contentDetails']['videoId'] for v in pl_res.get("items", [])]
        next_page = pl_res.get("nextPageToken")
        if not next_page:
            break

    total_views = 0
    total_likes = 0
    total_comments = 0

    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        vids_res = youtube.videos().list(
            part="statistics",
            id=",".join(batch)
        ).execute()
        for vid in vids_res.get("items", []):
            vstats = vid.get("statistics", {})
            total_views += int(vstats.get("viewCount", 0))
            total_likes += int(vstats.get("likeCount", 0))
            total_comments += int(vstats.get("commentCount", 0))

    return {
        "platform": "youtube",
        "account": channel_url,
        "views": total_views,
        "likes": total_likes,
        "comments": total_comments,
        "videos": len(video_ids),
        "subscribers": total_subscribers
    }
