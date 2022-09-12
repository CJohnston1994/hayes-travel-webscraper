from sqlalchemy import create_engine

HOLIDAY_XPATH = '//a[@class = "more color-white bg-yellow font-gotham"]'
CITY_XPATH = '//a[@class = "item shadow"]'
LOCATION_CONTAINER_XPATH = '//div[@class="hotel-info bg-white shadow"]'
DETAILS_CONTAINER_XPATH = '//*[@class="text"]'

# /html/body/div[4]/div/div/div[1]/div[3]/div[3]

'''DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = my_passwords.HOST
USER = 'postgres'
PASSWORD = my_passwords.PASSWORD
DATABASE = 'holiday_database'
PORT = 5432
ENGINE = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")'''

XPATH_DETAILS_DICTIONARY = { 
    "hotel": [LOCATION_CONTAINER_XPATH , "/h1"],
    "area": [LOCATION_CONTAINER_XPATH , "/div[2]"],
    "group_size": [DETAILS_CONTAINER_XPATH, '/div[1]//p'],
    "nights": [DETAILS_CONTAINER_XPATH, '/div[2]//p'],
    "catering": ['', '/div[3]//p'],
    "rating": ['', '//span[@class = "rating-label"]']
    }
