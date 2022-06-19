from dataclasses import dataclass
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os, json, uuid, pprint

class Scraper:
    def __init__(self):
        self.URL = "https://www.haystravel.co.uk/holiday-destinations"
        options = Options()
        options.add_argument("--headless")
        self.driver = Chrome(service=Service(ChromeDriverManager().install()), options = options) 
        self.wait = WebDriverWait(self.driver, 10)
        
    @dataclass
    class Holiday():
        url: str
        uuid: str
        deterministic_id: str
        hotel: str
        resort: str
        country: str
        holiday_price: int
        #group_size: int
        #duration: int
        #catering_type: str
        #soonest_departure: date
        star_rating: float
        #images: list

    def accept_cookies(self):
        '''
        Finds the Accept Cookies Button, waits for it to be clickable and then clicks it
        '''
        try:
            cookies_XPATH = (By.ID, 'onetrust-accept-btn-handler')
            cookies_btn = self.wait.until(EC.element_to_be_clickable(cookies_XPATH))
            cookies_btn.click()
            print("Cookies Done")
        except:
            print("Cookies Failed")

    def remove_empty_keys_from_list(self, dict:dict, list:list):
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
            country_name = elem.get_attribute('title')
            countries[country_name] = dest_link
        #logging.debug('countries finished')
        return countries
    
    def get_holidays_from_country(self, dict_of_countries:dict):
        '''
        Takes the country url dict and gets all the holidays hrefs from the urls for the countries

        '''
        #initialize/clear the list of countries without holidays
        countries_without_holidays = []
        #xpaths for the current project. Can be changed per site
        holiday_xpath = '//a[@class = "more color-white bg-yellow font-gotham"]'
        city_xpath = '//a[@class = "item shadow"]'

        #loop throught the countries gathered from the site
        for country in dict_of_countries:
            list_of_holidays = []
            #set the link of the holiday
            dest_link = dict_of_countries[country]
            #find the href attributess
            list_of_holidays = self.find_href(dest_link, holiday_xpath)
            #if there are no holidays available try looking for cities (site layout inconsistant)
            if len(list_of_holidays)<1:
                list_of_cities = self.find_href(dest_link, city_xpath)
                #if cities are found find holidays within
                for city in list_of_cities:
                    list_of_holidays = self.find_href(city, holiday_xpath)
            #if there are still no entries, set the 
            if len(list_of_holidays) < 1:
                countries_without_holidays.append(country)
            #assign the list to the current country in the dict
            dict_of_countries[country] = list_of_holidays
        #remove keys with no values
        dict_of_countries =  self.remove_empty_keys_from_list(dict_of_countries, countries_without_holidays)
        return dict_of_countries

    def find_href(self, url:str, xpath:str):
        '''
        finds hrefs on a given url using the xpath and returns a list of the hrefs 
        '''
        href_list = []
        self.driver.get(url)
        elems = self.driver.find_elements(By.XPATH, f'{xpath}')
        for elem in elems:
            dest_link = elem.get_attribute('href')
            href_list.append(dest_link)
        return href_list

    def save_to_json(self, data, file_name:str, folder_name:str, sub_folder_name:str=None):
        # get the working directory and append the file name arguemnts
        current_directory = os.getcwd()
        path = os.path.join(current_directory,folder_name, sub_folder_name)
        #create directory if it doesnt exist
        if not os.path.exists(path) and not os.path.isdir(path):
            os.mkdir(path)
        #attempt to write the data param to a json file
        try:
            os.chdir(path)
            if isinstance(data, dict):
                with open(file_name, 'w') as outfile:
                    #json_object = json.loads(data)                    
                    json.dump(data, outfile, indent = 6 )
            else:
                with open(file_name, 'w') as outfile:
                    json.write(data)
        #print a message if it fails
        except:
            print(f'Failed to save: {file_name} as JSON')
        
    def load_from_json(self, file_name:str, expected:type):
        with open(file_name) as json_file:
            data = json.load(json_file)
        if type(data) == expected:
            return data
        else:
            print("Data retrieval of file: ", file_name, " failed")
        
    def test_scrape(self, dict_of_countries:dict):
        '''
        early test to scrape a single page to check storage
        TODO - finish holiday scraper method
        '''
        holiday_list = []
        for country in dict_of_countries:
            self.driver.get(dict_of_countries[country][0])
            print(self.driver.current_url)
            current_holiday = self.Holiday(self.holiday_details(country))
            holiday_list.append(current_holiday)
        
    def holiday_details(self, country):
            location_container = self.holiday_container('//div[@class="hotel-info bg-white shadow"]')
            offer_details = self.holiday_container('//div[@class="text"]')
            print(location_container)
            url = self.driver.current_url
            holiday_id = str(uuid.uuid4())
            deterministic_id = url.replace("https://www.haystravel.co.uk/","")
            hotel = self.driver.find_element(By.XPATH, '//div[@class="resort color-yellow font-gotham"]').get_attribute('innerText')
            resort = self.driver.find_element(By.CLASS_NAME, 'resort').get_attribute('innerText')
            holiday_price = int(self.clean_price(self.driver.find_element(By.CLASS_NAME, 'price').get_attribute("innerText")))
            #group_size = self.driver.find_element(By.xpath, 'price'
            #duration = 
            #catering_type = 
            #soonest_departure = 
            star_rating = float(self.driver.find_element(By.XPATH, '//span[@class = "rating-label"]').text.rstrip("/5"))
            #holiday_details = [url, uuid, deterministic_id, hotel, resort, holiday_price, star_rating]
            #pprint.pprint(holiday_details)
            return self.Holiday(url, holiday_id, deterministic_id, hotel, resort, country, holiday_price, star_rating)

    def clean_price(self, price):
        #simply remove some specific characters left from the get attribute
        return price.replace("\n","").replace("\t","").replace("£","").replace("p","")
    '''    
    def holiday_container(self, container_xpath:str):
        #attempt to find the data container
        try:
            container = self.driver.find_elements(By.XPATH, container_xpath)
            container
            for item in container:
                print("container: ", item.get_attribute("innerText"))
            return container
        except:
            print("Container not found")
    '''
    
    def begin_scrape(self):
        self.driver.get(self.URL)
        self.accept_cookies()
        try:
            #country_dict = self.dict_countries()
            #final_dict = self.get_holidays_from_country(country_dict)
            #self.save_to_json(final_dict, "country_dict.json", 'country_dict', 'test2')
            final_dict = self.load_from_json("country_dict/test2/country_dict.json", dict)
            test = self.test_scrape(final_dict)
            pprint.pprint(test)
        finally:
            self.driver.quit()

if __name__ == "__main__":
    web_scraper = Scraper().begin_scrape()