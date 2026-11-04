import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime

BASE_URL = "https://iplaysoft.com"
MAX_FETCH = 50
JSON_FILE = "articles.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def load_exist():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"articles": []}

def save_json(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_img_tag(img, aid):
    src = img.get("src", "")
    # 补全相对路径为绝对地址
    if src.startswith("/"):
        src = BASE_URL + src
    img["src"] = src
    # 尝试绕过防盗链
    img["referrerpolicy"] = "no-referrer"
    # 前端兜底：图片加载失败浏览器自动替换占位图
    seed = f"ip_{aid}_{hash(src)%1000}"
    fallback_src = f"https://picsum.photos/seed/{seed}/800/450"
    img["onerror"] = f"this.src='{fallback_src}';this.onerror=null;"

def get_article_detail(url, aid):
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    content_div = soup.select_one(".post-content")
    if not content_div:
        return ""
    for img in content_div.find_all("img"):
        process_img_tag(img, aid)
    return str(content_div)

def main():
    exist_data = load_exist()
    exist_ids = {art["id"] for art in exist_data["articles"]}
    new_articles = []

    list_resp = requests.get(BASE_URL, headers=headers, timeout=15)
    list_resp.raise_for_status()
    soup = BeautifulSoup(list_resp.text, "html.parser")
    items = soup.select(".post-item")

    for item in items[:MAX_FETCH]:
        a_tag = item.select_one("h2 a")
        if not a_tag:
            continue
        title = a_tag.get_text(strip=True)
        link = a_tag["href"]
        if link.startswith("/"):
            link = BASE_URL + link

        match = re.search(r'/(\d+)\.html', link)
        if match:
            aid = int(match.group(1))
        else:
            aid = hash(link) % 1000000

        if aid in exist_ids:
            continue

        excerpt_el = item.select_one(".post-excerpt")
        excerpt = excerpt_el.get_text(strip=True) if excerpt_el else ""
        date_el = item.select_one(".post-date")
        pub_date = date_el.get_text(strip=True) if date_el else datetime.now().strftime("%Y-%m-%d")

        print(f"抓取：{title}")
        html_content = get_article_detail(link, aid)
        cover_seed = f"iplay_{aid}"

        art = {
            "id": aid,
            "title": title,
            "category": "软件资讯",
            "date": pub_date,
            "excerpt": excerpt,
            "coverSeed": cover_seed,
            "htmlContent": html_content
        }
        new_articles.append(art)

    exist_data["articles"] = new_articles + exist_data["articles"]
    exist_data["articles"] = exist_data["articles"][:300]
    save_json(exist_data)
    print(f"本次新增 {len(new_articles)} 篇文章")

if __name__ == "__main__":
    main()
