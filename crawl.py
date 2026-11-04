import json
import time
from playwright.async_api import async_playwright, TimeoutError

OUTPUT = "articles.json"

async def main():
    items = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="zh-CN"
        )
        page = await context.new_page()
        try:
            # 访问对外经贸大学主页
            await page.goto("https://www.uibe.edu.cn/", timeout=35000, wait_until="networkidle")
            # 定位贸大新闻板块的链接列表，用xpath匹配贸大新闻下新闻条目
            news_links = await page.locator("//h2[contains(text(),'贸大新闻')]/following-sibling::ul//a").all()
            print(f"✅ 检测到新闻数量：{len(news_links)}")
            for idx, link_el in enumerate(news_links[:15]):
                title = await link_el.inner_text()
                href = await link_el.get_attribute("href")
                # 补全相对url
                if href and not href.startswith("http"):
                    href = "https://www.uibe.edu.cn/" + href.lstrip("/")
                items.append({
                    "id": idx,
                    "title": title.strip(),
                    "category": "贸大新闻",
                    "date": time.strftime("%Y-%m-%d"),
                    "excerpt": "",
                    "coverSeed": "default",
                    "htmlContent": f"<p>原文：{href}</p>"
                })
        except TimeoutError:
            print("⚠️ 页面加载超时，本次无数据，保留旧文件")
        except Exception as e:
            print(f"⚠️ 抓取异常：{str(e)}")
        finally:
            await browser.close()

    # 只有抓到条目才写文件，空的时候不覆盖旧json
    if len(items) > 0:
        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"✅ 成功写入{len(items)}条新闻到 {OUTPUT}")
    else:
        print("ℹ️ 本次未获取新闻，不修改文件")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
