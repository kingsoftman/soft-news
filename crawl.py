import json
import requests
from bs4 import BeautifulSoup

OUTPUT = "articles.json"

def main():
    items = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    try:
        url = "https://www.bjeea.cn/html/selfstudy/"
        resp = requests.get(url, headers=headers, timeout=25)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        links = soup.select(".list01 li a")
        print(f"✅ 抓到 {len(links)} 条通知")
        for idx, a in enumerate(links[:15]):
            title = a.get_text(strip=True)
            href = a.get("href")
            if href and not href.startswith("http"):
                href = "https://www.bjeea.cn" + href
            items.append({
                "id": idx,
                "title": title,
                "category": "自考通知",
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