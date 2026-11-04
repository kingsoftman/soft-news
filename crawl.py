import asyncio
from playwright.async_api import async_playwright, TimeoutError

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        try:
            # 访问目标地址
            await page.goto("https://iplaysoft.com", timeout=30000)
            # 等待列表元素，捕获超时
            await page.wait_for_selector(".post-item", timeout=20000)
            items = page.locator(".post-item")
            count = await items.count()
            res_list = []
            for i in range(count):
                item = items.nth(i)
                title = await item.locator("h2 a").inner_text()
                link = await item.locator("h2 a").get_attribute("href")
                res_list.append({
                    "title": title,
                    "url": link
                })
            # 写入json
            import json
            with open("articles.json", "w", encoding="utf-8") as f:
                json.dump(res_list, f, ensure_ascii=False, indent=2)
            print(f"✅ 抓取成功，共 {count} 条")
        except TimeoutError:
            print("⚠️ 超时：没有找到 .post-item 列表，本次无更新，不报错退出")
            # 不修改原有json，直接保留旧文件
        except Exception as e:
            print(f"⚠️ 未知异常：{str(e)}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
