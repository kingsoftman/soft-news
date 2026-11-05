import json
import time
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

result_list = []
MAX_DEPTH = 3

def scan(page, url: str, depth: int = 0):
    if depth > MAX_DEPTH:
        return
    print(f"打开页面: {url}")
    try:
        page.goto(url, timeout=40000)
        # 等待页面网络空闲，h5ai加载数据
        page.wait_for_load_state("networkidle", timeout=30000)
        # 等待可见的 .entry 行，而不是等table
        page.wait_for_selector("tr.entry", timeout=25000, state="visible")
    except Exception as e:
        print(f"页面加载异常 {url} -> {e}")
        return

    rows = page.locator("tr.entry").all()
    for row in rows:
        a_tag = row.locator("td.name a")
        if not a_tag.count():
            continue
        href = a_tag.get_attribute("href")
        if href in ("../", "./", "_h5ai/"):
            continue
        name = a_tag.inner_text().strip()
        full_url = urljoin(url, href)
        mtime = row.locator("td.modified").inner_text().strip() if row.locator("td.modified").count() else ""
        size_str = row.locator("td.size").inner_text().strip() if row.locator("td.size").count() else ""
        is_dir = href.endswith("/")

        item = {
            "name": name,
            "url": full_url,
            "mtime": mtime,
            "size": size_str,
            "is_dir": is_dir
        }
        result_list.append(item)
        print(json.dumps(item, ensure_ascii=False))

        if is_dir:
            scan(page, full_url, depth + 1)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width":1280,"height":720}
        )
        page = context.new_page()
        base_url = "https://mirrors.lolinet.com/firmware/lenomola/"
        scan(page, base_url, depth=0)
        browser.close()

    with open("lenomola_meta.json", "w", encoding="utf-8") as f:
        json.dump(result_list, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 采集完成，一共 {len(result_list)} 条，保存 lenomola_meta.json")
