import requests
import time
import json
from bs4 import BeautifulSoup

HEADERS = {
    "User‑Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

result_list = []
MAX_DEPTH = 2   # lenomola：0层=lenomola根，1层=年份文件夹，2层=进入年份里面；不要调很大！

def scan(url: str, depth: int=0):
    if depth > MAX_DEPTH:
        return
    time.sleep(1.5)  # 限速，防止403封禁
    try:
        resp = requests.get(url, headers=HEADERS, timeout=25)
        resp.raise_for_status()
    except Exception as e:
        print(f"访问失败 {url} → {e}")
        return

    soup = BeautifulSoup(resp.text, "lxml")
    rows = soup.select("table tbody tr")

    for tr in rows:
        tds = tr.select("td")
        if len(tds) <3:
            continue
        td_name, td_mtime, td_size = tds[0], tds[1], tds[2]
        a_tag = td_name.find("a")
        if not a_tag:
            continue
        href = a_tag.get("href")
        if href in ("../", "./"):
            continue

        full_url = url + href
        name = a_tag.get_text(strip=True)
        mtime = td_mtime.get_text(strip=True)
        size_str = td_size.get_text(strip=True)
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
            scan(full_url, depth+1)

if __name__ == "__main__":
    base_url = "https://mirrors.lolinet.com/firmware/lenomola/"
    scan(base_url, depth=0)
    with open("lenomola_meta.json","w",encoding="utf‑8") as f:
        json.dump(result_list,f,ensure_ascii=False,indent=2)
    print(f"\n完成，共采集 {len(result_list)} 条元数据，保存 lenomola_meta.json")
