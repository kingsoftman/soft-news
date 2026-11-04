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
        for release in data:
            title = release["name"] or release["tag_name"]
            excerpt = release["body"][:120] + "..." if len(release["body"]) > 120 else release["body"]
            html = f"<p>{release['body']}</p><p>查看详情：<a href='{release['html_url']}'>{release['html_url']}</a></p>"
            items.append({
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
        for block in blocks:
            h2 = block.select_one("h2")
            if not h2:
                continue
            title = h2.get_text(strip=True)
            p = block.select_one("p")
            excerpt = p.get_text(strip=True) if p else ""
            html = str(block)
            items.append({
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

def main():
    list1 = fetch_magisk()
    list2 = fetch_lineageos()
    all_articles = list1 + list2
    # 只保留前10条
    all_articles = all_articles[:10]
    # 手动分配id
    for idx, item in enumerate(all_articles):
        item["id"] = idx + 1

    out = {"articles": all_articles}
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"✅ 抓取完成，最终输出 {len(all_articles)} 条")

if __name__ == "__main__":
    main()
