import imp
from webscraper import Scraper
import unittest

class WebscraperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.scraper = Scraper("https://www.haystravel.co.uk/holiday-destinations")
        country_dict = self.scraper.load_from_json("holiday_url_dict.json", "raw_data")
        self.test_dict = country_dict["Turkey"][0]
        self.test_holiday = self.scraper.Holiday()
    
    def test_get_holiday_details(self):
        expected_value = {
            "url": "https://www.haystravel.co.uk/grand-yazici-club-marmaris-palace",
            "uuid": "0a2325cf-0312-4d87-a736-8460f412a58f",
            "human_id": "grand-yazici-club-marmaris-palace",
            "hotel": "Grand yazici club marmaris palace",
            "area": "Marmaris, Turkey",
            "price": 589,
            "adults/children": [
                2
            ],
            "duration": 7,
            "catering": "All Inclusive",
            "next_date": "2022-10-13",
            "rating": 4.9,
            "images": [
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495858_grand-yazici-club-marmaris-palace07.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495838_grand-yazici-club-marmaris-palace01.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495842_grand-yazici-club-marmaris-palace02.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495845_grand-yazici-club-marmaris-palace03.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495848_grand-yazici-club-marmaris-palace04.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495851_grand-yazici-club-marmaris-palace05.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495855_grand-yazici-club-marmaris-palace06.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495858_grand-yazici-club-marmaris-palace07.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495838_grand-yazici-club-marmaris-palace01.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495842_grand-yazici-club-marmaris-palace02.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495845_grand-yazici-club-marmaris-palace03.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495848_grand-yazici-club-marmaris-palace04.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495851_grand-yazici-club-marmaris-palace05.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495855_grand-yazici-club-marmaris-palace06.jpg",
                "https://www.haystravel.co.uk/uploaded/2019/2/1550495858_grand-yazici-club-marmaris-palace07.jpg"
            ]
            }
        value = self.test()