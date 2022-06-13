from turtle import title
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pprint
import time


class Scraper:
    def __init__(self):
        self.URL = "https://www.haystravel.co.uk/holiday-destinations"
        options = Options()
        #options.add_argument("--headless")
        self.driver = Chrome(service=Service(ChromeDriverManager().install()), options = options) 
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

    def dict_cities(self, dict_of_countries: dict):
        '''
        1. Takes in the dict of country urls's. creates a new list from the keys in the dict
        2. Loops throught the country urls and visits each webpage
        3. Creates a dict using the cities as keys and the urls as the values
        4. returns the dict to be nested within the original dict
        '''
        print("list_area entered")
        dict_of_cities = {}
        list_of_countries = dict_of_countries.keys()
        for country in list_of_countries:
            self.driver.get(dict_of_countries[country])
            elems = self.driver.find_elements(By.XPATH, '//a[@class = "item shadow"]')
            for elem in elems:
                dest_link = elem.get_attribute("href")
                city = elem.get_attribute('title')
                dict_of_cities[city] = dest_link
            dict_of_countries[country] = dict_of_cities
        return dict_of_countries

    def dict_countries(self):
        '''
        Creates a dictionary, using the destination as a key and the URL as the value
        '''
        countries = {}
        elems = self.driver.find_elements(By.XPATH, '//a[@class = "item shadow"]')
        for elem in elems:
            dest_link = elem.get_attribute('href')
            country = elem.get_attribute('title')
            countries[country] = dest_link
        return countries


if __name__ == "__main__":
    try:
        web_scraper = Scraper()
        #print(web_scraper.driver.title)
        web_scraper.accept_cookies()
        country_dict = web_scraper.dict_countries()
        city_dict = web_scraper.dict_cities(country_dict)
        pprint.pprint(city_dict)
    finally:
        time.sleep(5)
        web_scraper.driver.quit()

