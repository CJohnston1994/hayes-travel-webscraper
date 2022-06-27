from webscraper import Scraper
import unittest

class WebscraperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.scraper = Scraper("https://www.haystravel.co.uk/holiday-destinations", False)
        self.country_dict = self.scraper.load_from_json("raw_data/src/country_urls.json", dict)
        self.holiday_dict = self.scraper.load_from_json("raw_data/src/holiday_url_dict.json", dict)
        self.test_dict = self.country_dict["Spain"][0]
        self.test_holiday = self.scraper.Holiday()
    
    def test_dict_countries(self):
        scraped_dict_countries = self.scraper.dict_countries()
        self.assertEqual(self.country_dict, scraped_dict_countries)

    def test_get_holidays_from_country(self):
        scraped_holidays = self.scraper.get_holidays_from_country(self.test_dict)
        self.assertEqual(scraped_holidays["Spain"],self.country_dict["Spain"])


unittest.main(exit=False, verbosity= 2)