from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pprint
import uuid

class Scraper:
    def __init__(self):
        self.URL = "https://www.haystravel.co.uk/holiday-destinations"
        options = Options()
        options.add_argument("--headless")
        self.driver = Chrome(service=Service(ChromeDriverManager().install()), options = options) 
        self.wait = WebDriverWait(self.driver, 10)

    class Holiday:
        def __init__(self, url):
            self.url = url
            self.deterministic_id = url.replace("https://www.haystravel.co.uk/","")
            self.uuid = str(uuid.uuid4())
            self.location = self.driver.find_elements(By.XPATH, '//div[@class = "resort color-yellow font-gotham"]')
            self.resort = self.driver.find_elements(By.XPATH, '//div[@class = "hotel color-blue mb-0"]')

        def holiday_details(self):
            holiday_details = [self.url, self.deterministic_id, self.uuid]
            return holiday_details
        
    def accept_cookies(self):
        '''
        Finds the Accept Cookies Button, waits for it to be clickable and then clicks it
        '''
        cookies_XPATH = (By.ID, 'onetrust-accept-btn-handler')
        cookies_btn = self.wait.until(EC.element_to_be_clickable(cookies_XPATH))
        cookies_btn.click()
        print("Cookies Done")

    def remove_empty_keys(self, dict:dict, list:list):
        for i in list:
            dict.pop(i,None)
        return dict

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
        #logging.debug('countries finished')
        return countries

    def get_holidays_by_country(self, dict_of_countries:dict):

        #using the keys of the original dict
        list_of_countries = dict_of_countries.keys()
        countries_without_holidays = []

        for country in list_of_countries:
            list_of_holidays = []
            #get each url within the original dict, using the key
            current_country_url = dict_of_countries[country]
            self.driver.get(current_country_url)
            #check for all holidays by XPATH
            try:
                #get the elements
                elems = self.driver.find_elements(By.XPATH , '//a[@class = "more color-white bg-yellow font-gotham"]')
                #wait until all elements have been located
                WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH , '//a[@class = "more color-white bg-yellow font-gotham"]')))
                for elem in elems:
                    #get the href link and append it to the holiday list
                    dest_link = elem.get_attribute('href')
                    this_holiday = self.Holiday(dest_link)
                    list_of_holidays.append(this_holiday.holiday_details())
            #if none are found in this area remove the key from the dict
            #in this case the some destinations are on an alternate url called hayesfaraway.co.uk
            except:
                #add to a list of emty keys in the country dict
                countries_without_holidays.append(country)
            #assign the list of holidays to the current country
            dict_of_countries[country] = list_of_holidays
        #remove the empty countries collected in the previous step
        dict_of_countries = self.remove_empty_keys(dict_of_countries,countries_without_holidays)
        return dict_of_countries

    def begin_scrape(self):
        self.driver.get(self.URL)
        try:
            self.accept_cookies()
            country_dict = self.dict_countries()
            final_dict = self.get_holidays_by_country(country_dict)
            pprint.pprint(final_dict)
        finally:
            self.driver.quit()


if __name__ == "__main__":
    web_scraper = Scraper().begin_scrape()