import requests
from bs4 import BeautifulSoup
import json
import os
import time

URL = "https://www.iplaysoft.com/"
OUTPUT = "articles.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.iplaysoft.com/"
}

def main():
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        items = []
        article_list = soup.select(".post-item")
        print(f"本次抓到 {len(article_list)} 篇文章")
        for idx, article in enumerate(article_list[:15]):
            title_tag = article.select_one("h2 a")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = title_tag["href"]
            excerpt_tag = article.select_one(".excerpt")
            excerpt = excerpt_tag.get_text(strip=True) if excerpt_tag else ""
            date_tag = article.select_one(".date")
            date = date_tag.get_text(strip=True) if date_tag else time.strftime("%Y-%m-%d")
            items.append({
                "id": idx,
                "title": title,
                "category": "安卓社区",
                "date": date,
                "excerpt": excerpt,
                "coverSeed": "default",
                "htmlContent": f"<p>{excerpt}</p><p>原文地址：{link}</p>"
            })
        # 写入文件
        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print("写入 articles.json 成功")
    except Exception as e:
        print(f"抓取异常：{e}")

if __name__ == "__main__":
    main()
