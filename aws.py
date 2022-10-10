import os, json, psycopg2, boto3, datetime
import config as c
import pandas as pd
from sqlalchemy import create_engine

class DataHandler():
    def __init__(self):
        #aws resources        
        s3_session = boto3.Session(aws_access_key_id=c.S3_ACCESS_KEY,aws_secret_access_key =c.S3_SECRET_KEY)
        self.s3_client = s3_session.client('s3')
        self.s3_resource = s3_session.resource('s3')
        self.my_bucket = self.s3_resource.Bucket('hayes-travel-web-scraper')

        self.engine = create_engine(f"{c.DATABASE_TYPE}+{c.DBAPI}://{c.USER}:{c.PASSWORD}@{c.HOST}:{c.PORT}/{c.DATABASE}")


    def _upload_data(self, df: pd.DataFrame):
        '''
        Upload all data and check for duplicate entries
        '''
        df = pd.DataFrame(df)
        for index, row in df.iterrows():
            file_name = os.path.join("raw_data", row["uuid"], 'data.json')
            self.s3_client.upload_file(file_name, 'hayes-travel-web-scraper', file_name)   
        
    def __send_data_to_rds(self, df: pd.DataFrame):
        self.engine.connect()
        df = pd.DataFrame.from_dict(df)
        df.to_sql(name='hayes_holiday', con=self.engine, if_exists='append')


    def __clean_and_normalize(self, data: list) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(data)
        
        pd.to_datetime(df.loc[0, 'next_date'])

        return df

    def __upload_images(self, raw_data):
        os.chdir('images')
        for image in os.listdir():
            image_file_name = os.path.join("raw_data",raw_data["uuid"],image)
            self.s3_client.upload_file(image, 'hayes-travel-web-scraper', image_file_name)   

    def images_already_scraped(self) -> list:
        scraped_images = []
        bucket = self.s3_resource.Bucket('hayes-travel-web-scraper')
        for file in bucket.objects.filter():
            if 'data.json' in file.key:
                content = file.get()['Body']
                json_content = json.load(content)
                if type(json_content) is str:
                    json_content = json.loads(json_content)
                
                scraped_url = json_content["images"]
                scraped_images.append(scraped_url)
        return scraped_images

    def drop_duplicates(self, df:  pd.DataFrame) -> pd.DataFrame:
        with psycopg2.connect(host=c.HOST, user=c.USER, password=c.PASSWORD, dbname=c.DATABASE, port=c.PORT) as conn:
            with conn.cursor() as curs:
                curs.execute(''' SELECT * FROM hayes_holiday ''')
                db_df = pd.DataFrame(curs.fetchall())
        dupe_subset = ['url', 'human_id', 'hotel', 'area', 'country', 'price', 'group_size', 'nights', 'catering', 'next_date']
        df.drop_duplicates(subset = dupe_subset)

        total_df = pd.concat([df,db_df])
        total_df.drop_duplicates(subset = dupe_subset)

        return total_df

    def process_data(self, raw_data):
        df = self.__clean_and_normalize(raw_data)
        dupe_free = self.drop_duplicates(df)
        self._upload_data(dupe_free)
        self.__send_data_to_rds(dupe_free)
        

    def process_images(self, path):
        original_path = os.getcwd()
        os.chdir(path)
        self.__upload_images(self.my_bucket)
        os.chdir(original_path)

    def remove_expired(self):
        today = datetime.date.today().strftime("%Y%m%d")
        with psycopg2.connect(host=c.HOST, user=c.USER, password=c.PASSWORD, dbname=c.DATABASE, port=c.PORT) as conn:
            with conn.cursor() as curs:
                curs.execute(f'''
                            CREATE TABLE IF NOT EXISTS expired_holidays AS
                                (SELECT * FROM hayes_holiday
                                WHERE next_date < '{today}');
                            INSERT INTO expired_holidays
                                SELECT * FROM hayes_holiday
                                WHERE uuid NOT IN (SELECT uuid FROM expired_holidays)
                                AND hayes_holiday.next_date < '{today}';
                            DELETE FROM hayes_holiday
                                WHERE hayes_holiday.next_date < '{today}';                      
                ''')

    def remove_duplicates(self):
        with psycopg2.connect(host=c.HOST, user=c.USER, password=c.PASSWORD, dbname=c.DATABASE, port=c.PORT) as conn:
            with conn.cursor() as curs:
                curs.execute('''
                CREATE TABLE distinct_store AS(
                SELECT DISTINCT on (url) test_table.* FROM test_table);
                DROP TABLE test_table;
                ALTER TABLE distinct_store
                    RENAME TO test_table;
                ''')
