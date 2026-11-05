import requests
import time
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://mirrors.lolinet.com/"
}

result_list = []
MAX_DEPTH = 3

def scan(url: str, depth: int = 0):
    if depth > MAX_DEPTH:
        return
    time.sleep(2)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=25)
        print(f"【{url}】 status={resp.status_code}")
        resp.raise_for_status()
    except Exception as e:
        print(f"访问失败 {url} → {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    rows = soup.select("tr.entry")
    for tr in rows:
        a_tag = tr.select_one("td.name a")
        if not a_tag:
            continue
        href = a_tag.get("href")
        if href in ("../", "./", "_h5ai/"):
            continue

        full_url = urljoin(url, href)
        name = a_tag.get_text(strip=True)
        mtime_el = tr.select_one("td.modified")
        size_el = tr.select_one("td.size")
        mtime = mtime_el.get_text(strip=True) if mtime_el else ""
        size_str = size_el.get_text(strip=True) if size_el else ""
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
            scan(full_url, depth + 1)

if __name__ == "__main__":
    base_url = "https://mirrors.lolinet.com/firmware/lenomola/"
    scan(base_url, depth=0)
    with open("lenomola_meta.json", "w", encoding="utf-8") as f:
        json.dump(result_list, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 完成，共采集 {len(result_list)} 条元数据，保存 lenomola_meta.json")
