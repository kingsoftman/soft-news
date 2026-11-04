import json
import asyncio
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
            await page.goto("https://httpbin.org/html", timeout=30000, wait_until="domcontentloaded")
            # 这个页面只有 h1 标题，拿来测试连通性
            title = await page.locator("h1").inner_text()
            items.append({
                "id": 1,
                "title": title.strip(),
                "category": "测试",
                "excerpt": "测试数据",
                "coverSeed": "default",
                "htmlContent": "<p>测试抓取成功</p>"
            })
            print("✅ 页面访问成功，拿到标题")
        except TimeoutError:
            print("⚠️ 超时，本次不更新json")
        except Exception as e:
            print(f"⚠️ 异常：{str(e)}")
        finally:
            await browser.close()

    if len(items) > 0:
        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"✅ 写入测试数据")
    else:
        print("ℹ️ 无数据，不修改文件")

if __name__ == "__main__":
    asyncio.run(main())
