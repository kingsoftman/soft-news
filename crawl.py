import json
import time
from playwright.sync_api import sync_playwright

OUTPUT = "articles.json"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="zh-CN"
        )
        page = context.new_page()
        page.goto("https://www.iplaysoft.com/", timeout=30000)
        page.wait_for_selector(".post-item", timeout=20000)

        items = []
        article_list = page.locator(".post-item").all()[:15]
        print(f"抓到 {len(article_list)} 篇")

        for idx, art in enumerate(article_list):
            title_tag = art.locator("h2 a")
            title = title_tag.inner_text().strip()
            link = title_tag.get_attribute("href")
            try:
                excerpt = art.locator(".excerpt").inner_text().strip()
            except:
                excerpt = ""
            try:
                date = art.locator(".date").inner_text().strip()
            except:
                date = time.strftime("%Y-%m-%d")

            items.append({
                "id": idx,
                "title": title,
                "category": "安卓社区",
                "date": date,
                "excerpt": excerpt,
                "coverSeed": "default",
                "htmlContent": f"<p>{excerpt}</p><p>原文：{link}</p>"
            })
        browser.close()

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print("写入成功")

if __name__ == "__main__":
    main()
