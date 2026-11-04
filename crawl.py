import json
from newspaper import Article
import requests

OUTPUT = "articles.json"

def main():
    items = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    try:
        # 先拿首页列表
        resp = requests.get("https://androidcommunity.com/", headers=headers, timeout=25)
        resp.raise_for_status()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "html.parser")
        a_list = soup.select("article h2 a")[:15]
        print(f"✅ 一共找到 {len(a_list)} 篇文章")

        for idx, a in enumerate(a_list):
            url = a.get("href")
            if not url:
                continue
            # newspaper3k自动提取标题、正文、封面图
            article = Article(url, headers=headers, timeout=20)
            article.download()
            article.parse()

            items.append({
                "id": idx,
                "title": article.title,
                "category": "安卓资讯",
                "excerpt": article.summary,
                "coverSeed": "default",
                "htmlContent": f"<p>{article.text[:500]}</p><p>原文：{url}</p>"
            })
    except Exception as e:
        print(f"⚠️ 抓取异常：{str(e)}")

    if items:
        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print("✅ 写入articles.json成功")
    else:
        print("ℹ️ 无数据，保留旧文件")

if __name__ == "__main__":
    main()
