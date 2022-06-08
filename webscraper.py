from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import pprint
import time

class Scraper:
    def __init__(self):
        self.URL = "https://www.haystravel.co.uk/holiday-destinations"
        options = Options().add_argument("--headless")
        self.driver = Chrome(ChromeDriverManager().install(), options=options)
        self.driver.implicitly_wait(5)
        self.driver.get(self.URL)
        self.wait = WebDriverWait(self.driver, 10)
        
    def accept_cookies(self):
        '''
        Finds the Accept Cookies Button, waits for it to be clickable and then clicks it
        '''
        cookies_XPATH = (By.ID, 'onetrust-accept-btn-handler')
        cookies_btn = self.wait.until(EC.element_to_be_clickable(cookies_XPATH))
        cookies_btn.click()
        print("Cookies Done")

    def list_areas(self, country):
        print("list_area entered")
        areas = {}
        url = f"https://www.haystravel.co.uk/destinations/{country}-holidays/"
        self.driver.find_element(By.LINK_TEXT, f"{country.capitalize()}").click()
        elems = self.driver.find_elements(By.XPATH, f'//a[contains(@href, "/{country}")]')
        pprint.pprint(elems)
        for elem in elems:
            dest_link = elem.get_attribute("@href")
            print()
            city = dest_link.replace(url, "").replace("/", " - ").replace("-", " ")
            areas[city] = dest_link
        print("areas returned")
        return areas

    def list_countries(self):
        '''
        Creates a dictionary, the key will be the destination and the content will be a nested dictonary with the sub areas and urls
        '''
        countries = {}
        elems = self.driver.find_elements(By.CLASS_NAME, 'item-shadow')
        for elem in elems:
            country = elem.get_attribute('title')
            countries[country] = self.list_areas(country)
        print("countries: ",countries)

if __name__ == "__main__":
    try:
        web_scraper = Scraper()
        print(web_scraper.driver.title)
        web_scraper.accept_cookies()
        web_scraper.list_countries()
    finally:
        time.sleep(5)
        web_scraper.driver.quit()

