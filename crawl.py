import requests
import json
import os

def fetch_pet_news():
    api_key = os.getenv("PETNEWS_APIKEY")
    if not api_key:
        raise Exception("缺少环境变量 PETNEWS_APIKEY，请配置仓库Secret")
    url = f"https://whyta.cn/api/tx/petnews?key={api_key}&num=20&rand=1"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    result = fetch_pet_news()
    with open("articles.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
