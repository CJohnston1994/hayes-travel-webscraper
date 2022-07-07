import webscraper as ws
import aws

if __name__ == "__main__":
    web_scraper = ws.Scraper("https://www.haystravel.co.uk/holiday-destinations", True)
    aws.upload_all_data()
