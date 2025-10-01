from playwright.sync_api import sync_playwright
import requests
import time

VK_SERVICE_TOKEN = "44205e6e44205e6e44205e6ebb471af3b24442044205e6e2cf56cd23ffa594a1ca339bd"
VK_API_VERSION = "5.131"

def extract_vk_id(profile_url: str) -> str:
    """
    Извлекает id или screen_name из ссылки VK.
    """
    if "vk.com/" in profile_url:
        return profile_url.rstrip("/").split("/")[-1]
    return profile_url

def get_vk_subscribers(vk_id: str) -> int:
    """
    Получает количество подписчиков пользователя через VK API.
    """
    try:
        url = "https://api.vk.com/method/users.get"
        params = {
            "user_ids": vk_id,
            "fields": "followers_count",
            "access_token": VK_SERVICE_TOKEN,
            "v": VK_API_VERSION
        }
        resp = requests.get(url, params=params).json()
        user_info = resp.get("response", [{}])[0]
        return user_info.get("followers_count", 0)
    except Exception as e:
        print("Ошибка получения подписчиков через VK API:", e)
        return 0

def get_vk_stats(profile_url: str) -> dict:
    vk_id = extract_vk_id(profile_url)
    
    stats = {
        "videos": 0,
        "views": 0,
        "likes": 0,
        "comments": 0,
        "subscribers": 0
    }

    stats["subscribers"] = get_vk_subscribers(vk_id)

    clips_url = f"https://vk.com/clips/{vk_id}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()   
        page.goto(clips_url, timeout=60000)
        page.wait_for_load_state("networkidle")

        view_elements = page.query_selector_all('h4[data-testid="clipcontainer-views"]')
        stats["videos"] = len(view_elements)
        for ve in view_elements:
            stats["views"] += int(''.join(filter(str.isdigit, ve.inner_text())))

        video_links = []    
        video_cards = page.query_selector_all('a[href*="/clip/"]')
        for card in video_cards:
            href = card.get_attribute("href")
            if href:
                if href.startswith("?"):
                    href = "https://vk.com/" + href
                video_links.append(href)

        for link in video_links:
            try:
                page.goto(link, timeout=60000)
                page.wait_for_load_state("networkidle")
                time.sleep(1)

                # Лайки
                like_el = page.query_selector('div[data-testid="clips-controls-like-count"]')
                if like_el:
                    stats["likes"] += int(''.join(filter(str.isdigit, like_el.inner_text())))

                # Комментарии
                comment_el = page.query_selector('span.vkuiHeader__indicator')
                if comment_el:
                    stats["comments"] += int(''.join(filter(str.isdigit, comment_el.inner_text())))

            except Exception as e:
                print(f"Ошибка при парсинге видео {link}: {e}")

        browser.close()

    return stats

profile_link = "https://vk.com/id1073025390"
print(get_vk_stats(profile_link))
