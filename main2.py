"""
中野エリアの賃貸情報を取得

- ページ遷移あり(10ページ分)
- csv書き出し（ローカル）
"""

import csv
import os
import requests
from bs4 import BeautifulSoup

# セッションの設定
session = requests.Session()
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
)


def scrape_pages(base_url, max_pages, writer):
    current_page = 1
    url = base_url
    while current_page <= max_pages:
        # ページの取得
        response = session.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # 必要な情報（例えば賃貸の名前と価格）の取得
        titles = soup.find_all(class_="cassetteitem_content-title")
        prices = soup.find_all(class_="cassetteitem_other-emphasis ui-text--bold")
        for title, price in zip(titles, prices):
            writer.writerow([title.text.strip(), price.text.strip()])

        # 「次へ」リンクを探す
        next_page_link = soup.find("a", text="次へ")
        if next_page_link and current_page < max_pages:
            url = response.url.rsplit("/", 4)[0] + next_page_link["href"]
            current_page += 1
        else:
            break  # 次のページがないか、最大ページ数に達した場合は終了


def main():
    base_url = "https://suumo.jp/chintai/tokyo/ek_27280/"
    max_pages = 10

    # フォルダとファイルの準備
    folder_path = "output"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, "rentals.csv")

    # CSVファイルへの書き出し準備
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["名前", "価格"])  # ヘッダーの書き込み
        scrape_pages(base_url, max_pages, writer)


if __name__ == "__main__":
    main()
