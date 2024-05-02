import csv
import os
import requests
from bs4 import BeautifulSoup


class Scraping:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
        )

    def scrape_and_export_csv(self):
        response = self.session.get(self.base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 特定のクラスを持つ全ての要素を検索
        elements = soup.find_all(class_="style-14mbwqe")

        # CSVファイルのパス設定
        folder_path = "output"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, "result1.csv")

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["TEXT", "URL"])  # CSVのヘッダー

            # 各要素からテキストとhref属性を抽出してCSVに書き込む
            for element in elements:
                text = element.get_text(strip=True)
                href = element.get("href")
                writer.writerow([text, href])


def main():
    base_url = "https://qiita.com/advent-calendar/2016/crawler"
    scraper = Scraping(base_url)
    scraper.scrape_and_export_csv()


if __name__ == "__main__":
    main()
