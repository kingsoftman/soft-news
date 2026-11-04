import json
from scrapling import Fetcher

OUTPUT = "articles.json"
fetcher = Fetcher(auto_match=False)

def main():
    items = []
    try:
        url = "https://androidcommunity.com/"
        page = fetcher.get(url, stealthy=True)
        article_list = page.css("article h2 a")
        print(f"✅ 抓到 {len(article_list)} 条资讯")
        for idx, a in enumerate(article_list[:15]):
            title = a.get_text(strip=True)
            href = a.attrib.get("href")
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
