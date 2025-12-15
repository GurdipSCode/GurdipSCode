import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from settings import CREDLY_USER, NUMBER_LAST_BADGES, README_FILE

class Credly:
    def __init__(self, username=None, number_badges=None, readme_file=None):
        self.BASE_URL = "https://www.credly.com"
        self.USER = username or CREDLY_USER or "pemtajo"
        self.NUMBER_BADGES = number_badges or NUMBER_LAST_BADGES or 0
        self.README_FILE = readme_file or README_FILE or "README.md"

    def get_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--silent")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def fetch_html(self):
        url = f"{self.BASE_URL}/users/{self.USER}"
        try:
            driver = self.get_webdriver()
            driver.get(url)
            WebDriverWait(driver, 15).until(
                lambda d: d.find_element(By.ID, "root").get_attribute("innerHTML").strip() != ""
            )
            time.sleep(3)
            html_content = driver.page_source
            driver.quit()
            return html_content
        except Exception:
            # fallback to requests
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text

    def extract_badges(self, html):
        soup = BeautifulSoup(html
