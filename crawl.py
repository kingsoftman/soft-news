import json
import requests
from bs4 import BeautifulSoup

OUTPUT = "articles.json"

def main():
    items = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    try:
        url = "https://androidcommunity.com/"
        resp = requests.get(url, headers=headers, timeout=25)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        # 首页文章卡片
        article_list = soup.select("article h2 a")
        print(f"✅ 抓到 {len(article_list)} 条资讯")
        for idx, a in enumerate(article_list[:15]):
            title = a.get_text(strip=True)
            href = a.get("href")
            items.append({
                "id": idx,
                "title": title,
                "category": "安卓资讯",
                "excerpt": "",
                "coverSeed": "default",
                "htmlContent": f"<p>原文地址：{href}</p>"
            })
    except Exception as e:
        print(f"⚠️ 抓取失败：{str(e)}")

    if items:
        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print("✅ 写入json完成")
    else:
        print("ℹ️ 无数据，保留旧文件")

if __name__ == "__main__":
    main()
