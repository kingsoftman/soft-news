import requests
import time
import json
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://mirrors.lolinet.com/"
}

result_list = []
MAX_DEPTH = 2

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
    # 直接拿页面全部a标签，不再限定tbody tr
    all_a = soup.find_all("a")
    for a_tag in all_a:
        href = a_tag.get("href")
        if not href:
            continue
        # 跳过上级、父目录
        if href in ("../", "./", "_h5ai/"):
            continue
        # 过滤掉锚点、外部链接
        if href.startswith("http"):
            continue

        full_url = url + href
        name = a_tag.get_text(strip=True)
        if not name:
            continue
        is_dir = href.endswith("/")

        # 取这个a的同行后面的时间、大小（h5ai布局：a后面跟着两个span）
        parent = a_tag.parent
        mtime = ""
        size_str = ""
        spans = parent.find_all("span")
        if len(spans)>=2:
            mtime = spans[0].get_text(strip=True)
            size_str = spans[1].get_text(strip=True)

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
