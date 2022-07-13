import boto3
import os

<<<<<<< Updated upstream
s3_client = boto3.client('s3')

raw_data = os.listdir('raw_data')
raw_data.remove('src')
os.chdir('raw_data')
base_dir = os.getcwd()

for folder in raw_data:
    
    os.chdir(folder)
    file_name = os.path.join( "raw_data", folder, 'data.json')
    s3_client.upload_file('data.json', 'hayes-travel-web-scraper', file_name)
    os.chdir(base_dir)

=======
import pandas as pd
import os, json
import psycopg2
from sqlalchemy import create_engine
from my_passwords import PASSWORD as pw

class DataHandler:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.raw_data = os.listdir('raw_data')
        os.chdir('raw_data')
        self.base_dir = os.getcwd()
        self.total_seen_list = []

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'hayes-travel-scraper.c3deqrfbkahl.us-east-1.rds.amazonaws.com'
        USER = 'postgres'
        PASSWORD = pw
        DATABASE = 'holiday_database'
        PORT = 5432
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

    def upload_all_data(self):
        '''
        Upload all data and check for duplicate entries
        '''
            
        for folder in self.raw_data:
            os.chdir(folder)
            file_name = os.path.join( "raw_data", folder, 'data.json')
            self.s3_client.upload_file('data.json', 'hayes-travel-web-scraper', file_name)
            image_path = os.path.join("raw_data", folder, 'images')
            os.chdir('images')
            for image in os.listdir():
                image_file_name = os.path.join("raw_data",folder,image)
                self.s3_client.upload_file(image, 'hayes-travel-web-scraper', image_file_name)
            os.chdir(self.base_dir)

    def not_in_seen_list(self, json_data):
        '''
        Add json datas to a seenlist and do no add if they match an existing element
        '''
        #check all elements in the list against the json
        for element in self.total_seen_list:
            if json_data['human_id' and 'next_date'] == element['human_id' and 'next_date']:
                return False
            else:
                self.seen_list.append()
        return True

    def clean_and_send_to_rds(self):
        self.engine.connect()

        init_dict = '/home/clark/Desktop/AICORE/Code/2.WebScraper/'
        raw_data_dict = os.path.join(init_dict, "raw_data")
        os.chdir(raw_data_dict)
        raw_data = os.listdir()
        raw_data.remove('src')
        for folder in raw_data:
            os.chdir(folder)
            with open('data.json') as json_data:
                init_json = json.load(json_data)
                init_json.popitem()
                new_json = self.clean(init_json)
                if self.not_in_seen_list(new_json):
                    new_json.to_sql('hayes-holiday',index=True, con=self.engine, if_exists='append')
            os.chdir(raw_data_dict)

    def clean(self, json_item):
        json_item['adults/children'] = sum(json_item['adults/children'])
        if json_item['adults/children'] == 22:
            json_item['adults/children'] = 4
        json_item['next_date'] = pd.to_datetime(json_item['next_date'], yearfirst=True)
        json_item = pd.json_normalize(json_item)
        json_item = json_item.astype(
            {'url': 'string',
            'uuid': 'string',
            'human_id': 'string',
            'hotel': 'string',
            'area': 'string',
            'country': 'string',
            'catering': 'string'
            })

        return json_item

    def check_database_for_duplicate(self, uuid4 ):
        sql = 'SELECT human_id, next_date FROM "hayes_holiday":'
        with psycopg2.connection.cursor as curs:
            curs.execute(sql)
>>>>>>> Stashed changes
