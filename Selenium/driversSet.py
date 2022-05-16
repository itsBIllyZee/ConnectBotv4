import logging
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
logging.basicConfig(handlers=[logging.FileHandler(filename="logs",
                                                  encoding='utf-8', mode='a')],
                    format="%(asctime)s %(name)s:%(levelname)s: %(message)s",
                    datefmt="%F %A %T",
                    level=logging.INFO)

class Selenium(webdriver.Chrome):
    def __init__(self, teardown=False, headless=False):
        self.log = logging.info
        self.debug = logging.error
        self.teardown = teardown
        self.options = webdriver.ChromeOptions()
        prefs = {"credentials_enable_service": False,
                 "profile.password_manager_enabled": False,
                 "profile.default_content_setting_values.geolocation": 2
                 }
        self.options.add_experimental_option("prefs", prefs)
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("--disable-features=ChromeWhatsNewUI")
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--disable-gpu")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_extension("Website/cjpalhdlnbpafiamejdnhcphjbkeiagm-1.42.4-Crx4Chrome.com.crx")
        super().__init__(options=self.options, service=Service(ChromeDriverManager().install()))


    def __exit__(self, exc_type, exc_val, exc_tb):
            if self.teardown:
                self.quit()
