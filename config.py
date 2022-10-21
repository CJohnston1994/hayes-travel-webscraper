import os

'''
AWS s3_client details
'''
S3_ACCESS = os.environ.get('S3_ACCESS_KEY')
S3_SECRET = os.environ.get('S3_SECRET_KEY')
S3_BUCKET = os.environ.get('BUCKET_NAME')

'''
SQLalchemy database engine details
'''
HOST = os.environ['HOST']
PASSWORD = os.environ["PASSWORD"]
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
USER = os.environ.get('DB_USER')
DATABASE = os.environ.get('DATABASE_NAME')
PORT = os.environ.get('PORT')

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