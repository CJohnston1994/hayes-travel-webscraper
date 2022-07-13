import os, json, psycopg2, boto3
import pandas as pd
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

    def upload(self, ):
        '''
        Upload all data and check for duplicate entries
        '''
            
        for folder in self.raw_data:
            os.chdir(folder)
            file_name = os.path.join("raw_data", folder, 'data.json')
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

    def send_to_rds(self, json_data):
        self.engine.connect()

        with open(json_data) as json_data:
            init_json = json.load(json_data)
            init_json.popitem()
            new_json = self.clean(init_json)
            if self.not_in_seen_list(new_json):
                new_json.to_sql('hayes-holiday',index=True, con=self.engine, if_exists='append')

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

    def check_database_for_duplicate(self, holiday_details):
        with psycopg2.connection.cursor as curs:
            curs.execute('''SELECT human_id, next_date
                        FROM 'hayes_holiday'            
            ''')
        records = curs.fetchall()
        if holiday_details['uuid'] and holiday_details['next_date'] in records:
            return True
        
    def prevent_image_rescrape(self, holiday_details):
        s3 = boto3.resource('s3')
        for file in self.s3_client:
            holiday_details['human_id']