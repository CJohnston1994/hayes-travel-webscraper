from fileinput import filename
from tempfile import mkdtemp, mkstemp
from webscraper.utils.webscraper import Scraper
import unittest, os, tempfile, shutil, json

class WebscraperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_scraper = Scraper("https://www.haystravel.co.uk/holiday-destinations", False)
        base_dir = '/home/clark/Desktop/AICORE/Code/2.WebScraper/'
        with open('json_data/country_urls.json') as  outfile:
            self.country_url_dict = json.load(outfile)
        with open ('json_data/holiday_url_dict.json') as outfile:
            self.holiday_url_dict = json.load(outfile)
        os.chdir(base_dir)
        self.working_dir = os.getcwd()
        #self.small_country_dict = self.test_scraper.load_from_json("tests/test_holiday_url_dict.json", dict)

    #@unittest.skip
    def test_dict_countries(self):
        scraped_dict_countries = self.test_scraper._scrape_countries_to_dict()
        self.assertIsInstance(scraped_dict_countries, dict)
        self.assertIn("Spain", scraped_dict_countries)

    #@unittest.skip
    def test_get_holidays_from_country(self):
        '''
        Can fail due to website changing, creating a difference from the stored data.
        '''
        scraped_holidays = self.test_scraper._scrape_holidays_from_country(self.country_url_dict)
        self.assertDictEqual(scraped_holidays,self.holiday_url_dict)
        self.assertIsInstance(scraped_holidays, dict)

    #@unittest.skip
    def test_find_href(self):
        href_output = self.test_scraper._find_href(self.test_scraper.URL, '//a[@class = "item shadow"]')
        self.assertIsInstance(href_output, list)
        self.assertEqual(href_output[0],self.country_url_dict["Spain"])
    
    #@unittest.skip
    def test_accept_cookies(self):
        incorrect_result = self.test_scraper._accept_cookies('Wrong Xpath')
        result = self.test_scraper._accept_cookies('onetrust-accept-btn-handler')
        self.assertFalse(incorrect_result)
        self.assertTrue(result)

    #@unittest.skip
    def test_remove_chars_convert_to_int(self):
        test_case_1 = ["2 Adults"]
        test_case_2 = "2 Adults + 2 Children".split(" + ")
        print(test_case_2)
        test_case_3 = ["1nt3g3r5"]

        test_result_1 = self.test_scraper._remove_chars_convert_to_int(test_case_1)
        test_result_2 = self.test_scraper._remove_chars_convert_to_int(test_case_2)
        test_result_3 = self.test_scraper._remove_chars_convert_to_int(test_case_3)

        print(test_result_1,test_result_2,test_result_3)

        self.assertEqual(test_result_1[0], 2)
        self.assertEqual(test_result_2, [2, 2])
        self.assertEquals(test_result_3[0], 1335)
        
    #@unittest.skip        
    def test_check_family_holiday(self):
        test_case_1 = "2 Adults"
        test_case_2 = "2 Adults + 2 Children"
        test_result_1 = self.test_scraper._check_family_holiday(test_case_1)
        test_result_2 = self.test_scraper._check_family_holiday(test_case_2)

        self.assertEquals(test_result_1, 2)
        self.assertEquals(test_result_2, 4)

    #@unittest.skip
    def test_convert_str_datetime(self):
        test_date_1 = "24th August 2077"

        result_1 = self.test_scraper._convert_str_to_datetime(test_date_1)
        
        self.assertEqual(str(result_1), "2077-08-24")
    
    #@unittest.skip
    def test_clean_datestring(self):

        test_date = "142nd Jullember 1962"
        with self.assertRaises(ValueError):
            self.test_scraper._convert_str_to_datetime(test_date)

'''
    def TearDown(self):
        self.test_scraper.driver.quit()
'''
unittest.main(exit=False, verbosity= 2)