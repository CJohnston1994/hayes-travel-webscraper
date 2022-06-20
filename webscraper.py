from dataclasses import dataclass
from datetime import date, datetime
from re import sub
from typing import Type
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os, json, uuid, pprint

class Scraper:
    def __init__(self, url):
        self.URL = url
        options = Options()
        options.add_argument("--headless")
        self.driver = Chrome(service=Service(ChromeDriverManager().install()), options = options) 
        self.wait = WebDriverWait(self.driver, 10)

    def __post_init__(self):
        self.begin_scrape()
        
    @dataclass
    class Holiday():
        details = {
        "url": str,
        "uuid": str,
        "human_id": str,
        "hotel": str,
        "area": str,
        "country": str,
        "price": int,
        "no_people": int,
        "nights": int,
        "catering": str,
        "next_ate": date,
        "rating": float,
        "images": list,
        }

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

    def save_to_json(self, data, file_name:str, folder_name:str, sub_folder_name:str=""):
        '''
        save a file as a json, with a specific path
        '''
        # get the working directory and append the file name arguemnts
        starting_directory = os.getcwd()
        dir_path = os.path.join(starting_directory,folder_name, sub_folder_name)
        #create directory if it doesnt exist
        if not os.path.exists(dir_path): #and not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        #attempt to write the data param to a json file
        try:
            os.chdir(dir_path)
            #check that the data is list or dict to dump
            if isinstance(data, dict) or isinstance(data, list):
                with open(file_name, 'w') as outfile:
                    #json_object = json.loads(data)                    
                    json.dump(data, outfile, indent = 4 )
            #strings will be written to the outfile
            else:
                with open(file_name, 'w') as outfile:
                    json.write(data)
                #cd to the starting directory
            os.chdir(starting_directory)
        #print a message if it fails
        except:
            print(f'Failed to save: {file_name} as JSON')
        
    def load_from_json(self, file_name:str, expected:type):
        with open(file_name) as json_file:
            data = json.load(json_file)
        try:
            if type(data) == expected:
                return data
            else:
                raise TypeError
        except TypeError:
               print("Data retrieval of file: ", file_name, " failed, incorrect type")

    def test_scrape(self, dict_of_countries:dict):
        '''
        early test to scrape a single page to check storage
        '''
        holiday_list = []
        for country in dict_of_countries:
            self.driver.get(dict_of_countries[country][0])
            current_holiday = self.Holiday()
            current_holiday.details["country"]= country
            self.holiday_details(current_holiday)
            
            holiday_list.append(current_holiday.details)
        return holiday_list
    
    def scrape_per_country(self, dict_of_countries):
        now = datetime.now()
        timestamp = now.strftime('%d-%m-%Y')
        for country in dict_of_countries:
            holiday_list = []
            for url in range(len(dict_of_countries[country])):
                country_len = len(dict_of_countries[country])
                self.driver.get(dict_of_countries[country][url])
                current_holiday = self.Holiday()
                current_holiday.details["country"]= country
                self.holiday_details(current_holiday)
                holiday_list.append(current_holiday.details)
            #/home/clark/Desktop/AICORE/Code/2.WebScraper/json_dumps/scraped_holidays
            self.save_to_json(holiday_list, f"{country}_holidays_{timestamp}.json","json_dumps", "scraped_holidays")
        
    def holiday_details(self, holiday:object):
        #create common container location
        location_container = '//div[@class="hotel-info bg-white shadow"]'
        details_container = '//div[@class="text"]'

        #all non details containers (including locations)
        url = self.driver.current_url
        holiday_id = str(uuid.uuid4())
        deterministic_id = url.replace("https://www.haystravel.co.uk/","")
        hotel = self.find_holiday_detail(location_container, '/h1')
        resort = self.find_holiday_detail(location_container, '/div[2]')

        #detail containers
        holiday_price = self.clean_price(self.find_holiday_detail("", '//div[@class="price color-blue"]'))
        group_size = self.find_holiday_detail(details_container, '/div[1]//p')
        duration = self.find_holiday_detail(details_container, '/div[2]//p')
        catering_type = self.find_holiday_detail(details_container, '/div[3]//p')
        soonest_departure = self.find_holiday_detail(details_container, '/div[5]//p[1]')
        star_rating = float(self.driver.find_element(By.XPATH, '//span[@class = "rating-label"]').text.rstrip("/5"))
        images = []
        images_element = self.driver.find_elements(By.XPATH, '//div[@class = "carousel-item"]/img')
        for image in images_element:
            src = image.get_attribute('src')
            images.append(src)

        holiday.details = {
            "url": url,
            "uuid": holiday_id,
            "human_id": deterministic_id,
            "hotel": hotel,
            "area": resort,
            "price": holiday_price,
            "no_people": group_size,
            "duration": duration,
            "catering": catering_type,
            "next_date": soonest_departure,
            "rating": star_rating,
            "images": images}
        return holiday

    def clean_price(self, price):
        #simply remove some specific characters left from the get attribute
        new_price = int(sub(r'[^\d.]', '', price))
        return new_price
        
    def find_holiday_detail(self, container:str, element_xpath:str):
        try:
            path = container + element_xpath
            element = self.driver.find_element(By.XPATH, path)
            #function takes 
            return element.get_attribute("innerText")
        except:
            print("element not found")

    def begin_scrape(self):
        self.driver.get(self.URL)
        self.accept_cookies()
        try:
            #country_dict = self.dict_countries()
            #url_dict = self.get_holidays_from_country(country_dict)
            #self.save_to_json(url_dict, "holiday_url_dict.json", 'json_dumps')
            url_dict = self.load_from_json("json_dumps/holiday_url_dict.json", dict)
            self.scrape_per_country(url_dict)

        finally:
            self.driver.quit()

if __name__ == "__main__":
    web_scraper = Scraper("https://www.haystravel.co.uk/holiday-destinations")