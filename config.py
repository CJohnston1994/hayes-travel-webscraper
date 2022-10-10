import os

'''test'''
S3_ACCESS_KEY='AKIAZM456EJJJOXJ7H6V'
S3_SECRET_KEY='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'
HOST='hayes-travel-scraper.c3deqrfbkahl.us-east-1.rds.amazonaws.com'
PASSWORD='Nicole2005!'

'''
AWS s3_client details
'''
#S3_ACCESS = os.environ.get('S3_ACCESS_KEY')
#S3_SECRET = os.environ.get('S3_SECRET_KEY')
S3_BUCKET = 'hayes-travel-web-scraper'

'''
SQLalchemy database engine details
'''
#HOST = os.environ['HOST']
#PASSWORD = os.environ["PASSWORD"]
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
USER = 'postgres'
DATABASE = 'holiday_database'
PORT = 5432

'''
XPATH CONSTANTS
'''

HOLIDAY_XPATH = '//a[@class = "more color-white bg-yellow font-gotham"]'
CITY_XPATH = '//a[@class = "item shadow"]'
LOCATION_CONTAINER_XPATH = '//div[@class="hotel-info bg-white shadow"]'
DETAILS_CONTAINER_XPATH = '//*[@class="text"]'

XPATH_DETAILS_DICTIONARY = { 
    "hotel": [LOCATION_CONTAINER_XPATH , "/h1"],
    "area": [LOCATION_CONTAINER_XPATH , "/div[2]"],
    "catering": [DETAILS_CONTAINER_XPATH, '/div[3]//p'],
    "rating": ['', '//span[@class = "rating-label"]']
    }