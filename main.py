"""
中野エリアの賃貸情報を取得

- ページ遷移なし
- csv書き出し（ローカル）
"""

import csv
import os
import requests
from bs4 import BeautifulSoup

# スクレイピングを行いたいページのURL
url = "https://suumo.jp/chintai/tokyo/ek_27280/"

# セッションを開始
session = requests.Session()
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
)

# サイトの情報を取得
response = session.get(url)
response.raise_for_status()

# HTMLコンテンツを解析
soup = BeautifulSoup(response.text, "html.parser")

# 賃貸の名前と価格を取得
titles = soup.find_all(class_="cassetteitem_content-title")
prices = soup.find_all(class_="cassetteitem_other-emphasis ui-text--bold")

# フォルダのパス
folder_path = "output"

# フォルダが存在しない場合は作成
os.makedirs(folder_path, exist_ok=True)

# ファイルパスの設定
file_path = os.path.join(folder_path, "rentals.csv")

# CSVファイルへの書き出し
with open(file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["名前", "価格"])  # ヘッダーの書き込み

    # 各賃貸の名前と価格を書き込む
    for title, price in zip(titles, prices):
        writer.writerow([title.text.strip(), price.text.strip()])
