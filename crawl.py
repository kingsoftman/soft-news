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
            # 北京教育考试院自考栏目
            await page.goto("https://www.bjeea.cn/html/selfstudy/", timeout=35000, wait_until="networkidle")
            # 列表选择器：页面里的新闻列表li>a
            links = await page.locator(".list01 li a").all()
            print(f"✅ 抓到链接数量：{len(links)}")
            for idx, link_el in enumerate(links[:15]):
                title = await link_el.inner_text()
                href = await link_el.get_attribute("href")
                if href and not href.startswith("http"):
                    href = "https://www.bjeea.cn" + href
                items.append({
                    "id": idx,
                    "title": title.strip(),
                    "category": "自考通知",
                    "excerpt": "",
                    "coverSeed": "default",
                    "htmlContent": f"<p>原文地址：{href}</p>"
                })
        except TimeoutError:
            print("⚠️ 页面加载超时，本次不更新文件，保留旧数据")
        except Exception as e:
            print(f"⚠️ 抓取异常：{str(e)}")
        finally:
            await browser.close()

    if len(items) > 0:
        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"✅ 写入 {len(items)} 条通知")
    else:
        print("ℹ️ 没有抓到数据，不修改json")

if __name__ == "__main__":
    asyncio.run(main())
