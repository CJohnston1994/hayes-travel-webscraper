import os
    
'''
AWS s3_client details
'''
S3_ACCESS = os.environ.get(os.env.S3_ACCESS_KEY)
S3_SECRET = os.environ.get(os.env.S3_SECRET_KEY)
S3_BUCKET = os.environ.get(os.env.BUCKET_NAME)

'''
SQLalchemy database engine details
'''
HOST = os.environ.get(os.env.HOST)
PASSWORD = os.environ.get(os.env.PASSWORD)
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
USER = os.environ.get(os.env.DB_USER)
DATABASE = os.environ.get(os.env.DB_NAME)
PORT = os.environ.get(os.env.DB_PORT)

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