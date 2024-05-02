"""
中野エリアの賃貸情報を取得

- ページ遷移あり(10ページ分)
- スプレッドシート書き出し（クラウド）
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup


class Scraping:
    def __init__(self, base_url, max_page):
        self.base_url = base_url
        self.max_page = max_page
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
        )

    def scrape_pages(self):
        data = []
        current_page = 1
        url = self.base_url
        while current_page <= self.max_page:
            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            titles = soup.find_all(class_="cassetteitem_content-title")
            prices = soup.find_all(class_="cassetteitem_other-emphasis ui-text--bold")

            for title, price in zip(titles, prices):
                data.append([title.text.strip(), price.text.strip()])

            next_page_link = soup.find("a", text="次へ")
            if next_page_link and current_page < self.max_page:
                url = response.url.rsplit("/", 1)[0] + "/" + next_page_link.get("href")
                current_page += 1
            else:
                break

        return data

    def export_sheet(self, data):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "client_secret.json", scope
        )
        client = gspread.authorize(creds)

        sheet = client.open("Nakano Rentals").sheet1
        sheet.append_row(["Name", "Price"])
        for row in data:
            sheet.append_row(row)


def main():
    base_url = "https://suumo.jp/chintai/tokyo/ek_27280/"
    max_pages = 10
    scraper = Scraping(base_url, max_pages)
    rental_data = scraper.scrape_pages()
    scraper.export_sheet(rental_data)


if __name__ == "__main__":
    main()
