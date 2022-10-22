import os, json, uuid, time, random,  shutil, re
from utils.aws import DataHandler
import utils.config as c
from dataclasses import dataclass
from genericpath import exists
from re import sub
from urllib.request import urlretrieve
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from typing import ClassVar

class Scraper:
    def __init__(self, url: str, autoscrape:bool = True ):
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        self.URL = url
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'user-agent={user_agent}')
        self.driver = Chrome(service=Service(ChromeDriverManager().install()), options = options)
        self.driver.get(self.URL)
        self.wait = WebDriverWait(self.driver, 10)
        self.data_handler = DataHandler()            
        if not exists("raw_data"):
            os.mkdir("raw_data")
        if autoscrape:
            self.run_scraper()

    @dataclass
    class _Holiday():
        url: ClassVar[str] = None
        uuid: ClassVar[str] = None
        human_id: ClassVar[str] = None
        hotel: ClassVar[str] = None
        area: ClassVar[str] = None
        country: ClassVar[str] = None
        price: ClassVar[int] = None
        group_size: ClassVar[list] = None
        nights: ClassVar[int] = None
        catering: ClassVar[str] = None
        next_date: ClassVar[str] = None
        rating: ClassVar[float] = None
        images: ClassVar[list] = None

    def _accept_cookies(self, xpath) -> bool:
        '''
        Finds the Accept Cookies Button, waits for it to be clickable and then clicks it
        '''
        try:
            cookies_XPATH = (By.ID, xpath)
            cookies_btn = self.wait.until(EC.element_to_be_clickable(cookies_XPATH))
            time.sleep(1)
            cookies_btn.click()
            return True
        except Exception:
            print("Failed to accept cookies")

    def __remove_dict_keys_from_list(
        self, 
        dict:dict, 
        list:list
        ) -> dict:
        '''
        remove all dict entries form a list passed in, this list should be empty keys
        '''
        for link in list:
            dict.pop(link,None)
        return dict

    def _scrape_countries_to_dict(self) -> dict:
        '''
        Creates a dictionary, using the country as a key and URL as the value
        '''

        #create an empty dict to retrun
        countries = {}
        elems = self.driver.find_elements(By.XPATH, '//a[@class = "item shadow"]')
        for elem in elems:
            #get the href, then get the title attribute from it. then add the key and value to the dictionary
            dest_link = elem.get_attribute('href')
            country_name = elem.get_attribute('title')
            countries[country_name] = dest_link
        if not exists("json_data"):
            os.mkdir("json_data")
        with open("json_data/country_urls.json","w") as outfile:
            json.dump(countries, outfile, indent=4)
        return countries
    
    def _scrape_holidays_from_country(self, dict_of_countries:dict) -> dict:
        '''
        Takes the country url dict and gets all the holidays hrefs from the urls for the countries
        '''
        #initialize/clear the list of countries without holidays
        countries_without_holidays = []
        #xpaths for the current project. Can be changed per site
        holiday_xpath = c.HOLIDAY_XPATH
        city_xpath = c.CITY_XPATH

        #loop throught the countries gathered from the site

        for country, dest_link in dict_of_countries.items():
            list_of_holidays = []
            try:
                #find the href attributes
                list_of_holidays = self._find_href(dest_link, holiday_xpath)
                #if there are no holidays available try looking for cities (site layout inconsistant)
                if len(list_of_holidays)<1:
                    list_of_cities = self._find_href(dest_link, city_xpath)
                    #if cities are found find holidays within
                    for city in list_of_cities:
                        list_of_holidays = self._find_href(city, holiday_xpath)
                #if there are still no entries, set the country to be removed from the dict
                if len(list_of_holidays) < 1:
                    countries_without_holidays.append(country)
                #assign the list to the current country in the dict
                dict_of_countries[country] = list_of_holidays
            except TypeError:
                return dict_of_countries
        #remove keys with no values
        dict_of_countries =  self.__remove_dict_keys_from_list(dict_of_countries, countries_without_holidays)
        with open("json_data/holiday_url_dict.json", "w") as outfile:
            json.dump(dict_of_countries, outfile, indent=4)
        return dict_of_countries

    def _find_href(
                self, 
                url: str,
                xpath: str
                ) -> list:
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


    def __scrape_each_country(self, dict_of_countries:dict):
        '''
        navigate to the holiday url and create the holiday data object
        gets the datails and assign them to the dict entry
        create the list(dict.fromkeys(countries)path for saving the holiday
        returns nothing
        Scrape the holiday data
        nested for loop is used to set country as it was not reliably scrapable from
        the holiday url itslef
        '''
        total_list = []
        countries = dict_of_countries.keys()
        for country in countries:
            for holiday in dict_of_countries[country]:
                # scrapes details
                self.driver.get(holiday)
                current_holiday = self._Holiday()
                try:
                    self.__get_holiday_details(current_holiday, country)
                except Exception as e:
                    continue
                holiday_path = os.path.join("raw_data", f'{current_holiday.uuid}')
                if not exists(holiday_path):
                    os.mkdir(holiday_path)
                image_path = os.path.join(holiday_path, "images")
                if not exists(image_path):
                    os.mkdir(image_path)
                with open(os.path.join(holiday_path,"data.json"), "w") as outfile:
                    json.dump(current_holiday.__dict__, outfile, indent=4, default=str)

                total_list.append(current_holiday.__dict__)

            print(f"{country} scrape completed!")
        return total_list
        
    
    def __scrape_images(self, dataframe_list):
        '''
        gathers image urls form the scraped list of images
        scrape every im
        Scrape 3 images for each holiday into an image folder within the uuid folder created in scrape_per_country
        '''
        for _dict in dataframe_list:
            address_path = os.path.join("raw_data", _dict["uuid"], "images")
            for element in range(3):
                image_link = _dict["images"][element]
                
                save_name = os.path.join(address_path, re.sub(r'^.+/([^/]+)$', r'\1', image_link))
                urlretrieve(image_link, save_name)
                time.sleep(random.randint(0,3))

        
    def __get_holiday_details(
        self,
        holiday: object, 
        country: str
        ):

        '''
        This method collects details from each holiday url
        using selenium to scrape the webpage for the details.
        each detail is then attached to the Holiday dataclass using the setattr method
        to remove some redunant code a dict was used in the config file to pass multiple attributes at once.

        '''
        page_url = self.driver.current_url
        deterministic_id = page_url.replace("https://www.haystravel.co.uk/","")
        try:
            area = self._find_holiday_detail(c.LOCATION_CONTAINER_XPATH, '/div[2]')
            hotel = self._find_holiday_detail(c.LOCATION_CONTAINER_XPATH, '/h1')
        except Exception:
            area = None
            hotel = deterministic_id.replace("-", " ")

        self._find_holiday_detail(c.DETAILS_CONTAINER_XPATH, '/div[1]//p')
        group_size = self._find_holiday_detail(c.DETAILS_CONTAINER_XPATH, '/div[1]//p')
        duration = self._find_holiday_detail(c.DETAILS_CONTAINER_XPATH, '/div[2]//p')
        soonest_departure = self._find_holiday_detail(c.DETAILS_CONTAINER_XPATH, '/div[5]//p[1]')
        images = set()
        images_element = self.driver.find_elements(By.XPATH, '//div[@class = "carousel-item"]/img')
        for image in images_element:
            src = image.get_attribute('src')
            images.add(src)

        #setting attributes for elements that need more processing, or that can't be scraped
        setattr(holiday, "url", self.driver.current_url)
        setattr(holiday, "uuid", str(uuid.uuid4()))
        setattr(holiday, "country", country)
        setattr(holiday, "hotel", hotel)
        setattr(holiday, "area", area)
        setattr(holiday, "human_id", deterministic_id)
        setattr(holiday, "price", self._remove_chars_convert_to_int(self._find_holiday_detail("", '//div[@class="price color-blue"]')))
        setattr(holiday, "group_size", self._check_family_holiday(group_size))
        setattr(holiday, "nights", self._remove_chars_convert_to_int(duration))
        setattr(holiday, "next_date", self._convert_str_to_datetime(soonest_departure))
        setattr(holiday, "images", list(images))

        #loop through the dict values in the config file and set attributes for each key
        for key, value in list(c.XPATH_DETAILS_DICTIONARY.items()):
            setattr(holiday, key, self._find_holiday_detail(value[0], value[1]))
       
     
    def _convert_str_to_datetime(self, date_string: str) -> str:
        '''
        convert string returned from _clean_date_string to datetime format
        using a using  the clean_date_string method
        '''
        try:
            return self._clean_date_string(date_string)
        except ValueError as e:
            print(e)
            raise ValueError('Invalid date string') from e

    def _clean_date_string(self, date_string):
        '''
        remove characters from the day use dict to change month to number
        converts month word
        convert the month to numberdate
        remove date subscripts
        '''        
        new_date = date_string.split(" ")
        new_date[0] = new_date[0].rstrip("stndrh")
        new_date = " ".join(new_date)
        try:        
            return datetime.strptime(new_date, '%d %B %Y').date()
        except ValueError as e:
            raise ValueError("Invalid date string") from e
            
            

    def _remove_chars_convert_to_int(self, group_size):
        '''
        remove characters to convert strings from get_attribute("innerText") to ints
        allowing for easier datacleaning. This is done by subbing all non numeric characters
        leaving us with only numbers which are converted to integers. This handles
        both strings and lists of strings
        '''
        if isinstance(group_size, list):
            new_int_list = []
            for num in group_size:
                new_int = sub(r'[^\d.]', '', num)
                new_int_list.append(new_int)
            return list(map(int, new_int_list))
        else:
            new_int = int(sub(r'[^\d.]', '', group_size))
            return new_int
            
    def _check_family_holiday(self, group_size: str):
        '''
        if there are Adults and children in a holiday deal split this into a list of 2 entries
        to be converted into ints
        '''

        no_people = self._remove_chars_convert_to_int(group_size.split(' + '))
        
        return sum(no_people) if type(no_people) == list else no_people
        
    def _find_holiday_detail(self, container: str, element_xpath: str):
        '''
        Find details by relative xpath given a container and element
        in the url given by self.driver.geturl(), generalising the process
        of getting href attributes.
        '''
        try:
            path = container + element_xpath
            if not (element:= self.driver.find_element(By.XPATH, path)):
                raise TypeError
            return element.get_attribute("innerText")
        except Exception as e:
            print(f"element not found\n Error: {e}\n")
    
    def run_scraper(self):
        '''
        Main Scraping of the program
        '''
        self._accept_cookies('onetrust-accept-btn-handler')
        country_dict = self._scrape_countries_to_dict()
        url_dict = self._scrape_holidays_from_country(country_dict)
        dataframe_list = self.__scrape_each_country(url_dict)
        self.data_handler.process_data(dataframe_list)
        #self.__scrape_images(dataframe_list)
        print("Scrape Complete")
        self.data_handler.remove_expired()
        print("Expired Deals removed")
        shutil.rmtree('raw_data')
        print("Local data cleared")