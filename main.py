from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ScreenshotTaker:
    def __init__(self):
        # WebDriverの初期化をコンストラクタで行います
        webdriver_path = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(service=Service(webdriver_path))

    def take_screenshot(self, url, save_file_path):
        # 指定したURLにアクセス
        self.driver.get(url)

        # スクリーンショットを撮影
        self.driver.save_screenshot(save_file_path)

    def close_browser(self):
        # ブラウザを閉じる
        self.driver.quit()


def main():
    taker = ScreenshotTaker()
    try:
        taker.take_screenshot("https://www.google.com", "screenshot.png")
    finally:
        # エラーが発生してもブラウザが閉じられるようにする
        taker.close_browser()


if __name__ == "__main__":
    main()
