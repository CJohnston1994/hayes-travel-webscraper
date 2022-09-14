from distutils import core
import config, os, json, psycopg2, boto3
from sys import prefix
import pandas as pd
from sqlalchemy import create_engine

class DataHandler:
    def __init__(self):
        self.s3_client = boto3.resource('s3')
        self.total_seen_list = []
        self.engine = config.ENGINE
        '''with open('mypasswords.yml') as mypasswd:
        credentials = yaml.safe_load(mypasswd)
        HOST = credentials['HOST']
        PASSWORD = credentials['PASSWORD']
        DATABASE_TYPE = credentials['DATABASE_TYPE']
        DBAPI =  credentials['DBAPI']
        USER = credentials['USER']
        DATABASE = credentials['DATABASE']
        PORT = credentials['PORT']'''

    def _upload_data(self, raw_data):
        '''
        Upload all data and check for duplicate entries
        '''
        
        file_name = os.path.join("raw_data", raw_data["uuid"], 'data.json')
        self.s3_client.upload_file('data.json', 'hayes-travel-web-scraper', file_name)   
        
    def __not_in_seen_list(self, json_data):
        '''
        Add json data to a seenlist and do not add if they match an existing element
        '''
        #check all elements in the list against the json
        humanId_list = any(json_data['human_id'] for _ in self.total_seen_list)
        next_date_list = any(json_data['next_date'] for _ in self.total_seen_list)

        if humanId_list and next_date_list:
            return False
        else:
            self.seen_list.append()
        return True


    def __send_data_to_rds(self, json_data):
        self.engine.connect()

        with open(json_data) as json_data:
            init_json = json.load(json_data)
            init_json.popitem()
            new_json = self.clean(init_json)
            if self.not_in_seen_list(new_json):
                new_json.to_sql('hayes-holiday',index=True, con=self.engine, if_exists='append')

    def __clean(self, json_item):
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

    def __check_rds_for_duplicate(self, cleaned_data):
        self.s3_client()

    def __check_database_for_duplicate(self, cleaned_data):
        with psycopg2.connection.cursor as curs:
            curs.execute('''SELECT human_id, next_date
                        FROM 'hayes_holiday'            
            ''')
        records = curs.fetchall()
        if cleaned_data['uuid'] and cleaned_data['next_date'] in records:
            return True

    def __upload_images(self, raw_data):
        os.chdir('images')
        for image in os.listdir():
            image_file_name = os.path.join("raw_data",raw_data["uuid"],image)
            self.s3_client.upload_file(image, 'hayes-travel-web-scraper', image_file_name)
        os.chdir(self.base_dir)        

    def images_already_scraped(self, bucket):
        scraped_images = []
        for file in bucket.objects.filter():
            if 'data.json' in file.key:
                content = file.get()['Body']
                json_content = json.load(content)
                scraped_url = json_content["images"]
                scraped_images += scraped_url
        return scraped_images

    def process_data(self, raw_data):
        clean_data = self.__clean(raw_data)
        my_bucket = self.s3_client.Bucket('hayes-travel-web-scraper')
        if clean_data['uuid'] not in my_bucket.objects.filter():
            self.__send_data_to_rds(clean_data)
        if not self.__check_database_for_duplicate(clean_data):
            self._upload_data(clean_data)

    def process_images(self, path : str):        
        if self.images_already_scraped(path):
            self.__upload_images()