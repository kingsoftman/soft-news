import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

OUTPUT = "articles.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_magisk():
    items = []
    try:
        url = "https://api.github.com/repos/topjohnwu/Magisk/releases"
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        for idx, release in enumerate(data[:4]):
            title = release["name"] or release["tag_name"]
            excerpt = release["body"][:120] + "..." if len(release["body"]) > 120 else release["body"]
            html = f"<p>{release['body']}</p><p>查看详情：<a href='{release['html_url']}'>{release['html_url']}</a></p>"
            items.append({
                "id": idx + 1,
                "title": f"Magisk - {title}",
                "category": "刷机资讯",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "excerpt": excerpt,
                "coverSeed": "default",
                "htmlContent": html
            })
    except Exception as e:
        print(f"Magisk抓取失败: {e}")
    return items

def fetch_lineageos():
    items = []
    try:
        url = "https://lineageos.org/changelog/"
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        blocks = soup.select("article")
        for idx, block in enumerate(blocks[:4]):
            h2 = block.select_one("h2")
            if not h2:
                continue
            title = h2.get_text(strip=True)
            p = block.select_one("p")
            excerpt = p.get_text(strip=True) if p else ""
            html = str(block)
            items.append({
                "id": 100 + idx + 1,
                "title": f"LineageOS - {title}",
                "category": "刷机资讯",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "excerpt": excerpt,
                "coverSeed": "default",
                "htmlContent": html
            })
    except Exception as e:
        print(f"LineageOS抓取失败: {e}")
    return items

def fetch_xda():
    items = []
    try:
        # XDA 首页最新帖子列表
        url = "https://forum.xda-developers.com/latest/"
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        threads = soup.select(".structItem-title a")
        for idx, a in enumerate(threads[:4]):
            title = a.get_text(strip=True)
            link = a.get("href", "")
            if link.startswith("/"):
                link = "https://forum.xda-developers.com" + link
            excerpt = "XDA社区最新刷机讨论帖"
            html = f"<p>帖子标题：{title}</p><p>访问原帖：<a href='{link}'>{link}</a></p>"
            items.append({
                "id": 200 + idx + 1,
                "title": f"XDA - {title}",
                "category": "刷机资讯",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "excerpt": excerpt,
                "coverSeed": "default",
                "htmlContent": html
            })
    except Exception as e:
        print(f"XDA抓取失败: {e}")
    return items

def main():
    list1 = fetch_magisk()
    list2 = fetch_lineageos()
    list3 = fetch_xda()
    all_articles = list1 + list2 + list3
    out = {"articles": all_articles}
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"✅ 抓取完成，一共 {len(all_articles)} 条")

if __name__ == "__main__":
    main()
