import os, json, psycopg2, boto3, datetime
import utils.config as c
import pandas as pd
from sqlalchemy import create_engine, inspect

class DataHandler():
    def __init__(self):
        #aws resources        
        s3_session = boto3.Session(aws_access_key_id=c.S3_ACCESS,aws_secret_access_key =c.S3_SECRET)
        self.s3_client = s3_session.client('s3')
        self.s3_resource = s3_session.resource('s3')
        self.my_bucket = self.s3_resource.Bucket('hayes-travel-web-scraper')

        self.engine = create_engine(f"{c.DATABASE_TYPE}+{c.DBAPI}://{c.USER}:{c.PASSWORD}@{c.HOST}:{c.PORT}/{c.DATABASE}")
        

    def table_check_create_if_not_exist(self):
        '''
        Use an SQLAlchemy inspect object to check if the holiday table exists.
        '''
        ins = inspect(self.engine)
        return ins.has_table(self.engine.connect(),'hayes_holiday')

    def _upload_data(self, df: pd.DataFrame):
        '''
        Upload all data and check for duplicate entries
        '''
        df = pd.DataFrame(df)
        for index, row in df.iterrows():
            file_name = os.path.join("raw_data", row["uuid"], 'data.json')
            self.s3_client.upload_file(file_name, 'hayes-travel-web-scraper', file_name)

        
        
    def __send_data_to_rds(self, df: pd.DataFrame):
        '''
        Connect to the RDS and push the pandas dataframe using the sqlalchemy engine
        '''
        self.engine.connect()
        df = pd.DataFrame.from_dict(df)
        df.to_sql(name='hayes_holiday', con=self.engine, if_exists='append')


    def __clean_and_normalize(self, data: list) -> pd.DataFrame:
        '''
        make sure data is in Dataframe format
        change next_date column to datetime
        and return data
        '''
        df = pd.DataFrame.from_dict(data)
        pd.to_datetime(df.loc[0, 'next_date'])

        return df

    def __upload_images(self, raw_data):
        '''
        connect to s3 bucket ussing boto3
        upload images under holiday uuid folders
        '''
        os.chdir('images')
        for image in os.listdir():
            image_file_name = os.path.join("raw_data",raw_data["uuid"],image)
            self.s3_client.upload_file(image, 'hayes-travel-web-scraper', image_file_name)   

    def images_already_scraped(self) -> list:
        '''
        Check for images that have already been scraped
        TODO - get hotel list from database and check s3_resource for matching hotels
        remove images from by hotel
        '''
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

        '''
        Takes in a pandas DataFrame
        connects to the database and pulls all data
        appends the dataframe with the database
        drop the duplicates that match all rows as holidays can have some variants
        return the new dataframe
        '''

        with psycopg2.connect(host=c.HOST, user=c.USER, password=c.PASSWORD, dbname=c.DATABASE, port=c.PORT) as conn:
            with conn.cursor() as curs:
                curs.execute(''' SELECT * FROM hayes_holiday ''')
                db_df = pd.DataFrame(curs.fetchall())
                total_df = df.append(db_df)

        df.drop_duplicates()
        print(df)

        return total_df

    def process_data(self, raw_data):

        '''
        Method containing the data processing methods.
        The data in cleaned, a check is then done for the existence of the database table
        If the table does not exist it is created using the pandas.to_sql function in __send_data_to_rds
        otherwise the data is appended to a dataframe containing the entire holidays table.
        The holidays table is kept small by removing expired  holidays and duplicates each time the scraper runs.
        the appended data is then cleared of duplicates and send to the rds.

        '''
        clean_df = self.__clean_and_normalize(raw_data)
        if table_exists := self.table_check_create_if_not_exist():
            dupe_free = self.drop_duplicates(clean_df)
            self.__send_data_to_rds(dupe_free)
            self._upload_data(dupe_free)        
        else:
            self.__send_data_to_rds(clean_df)
            self._upload_data(clean_df)    
            

    def process_images(self, path):
        '''
        method containing the unused code for processing the imges scraped by the scraper.
        after above todo is completed this code can be implemented without scraping multiple
        copies of the same images.
        '''
        original_path = os.getcwd()
        os.chdir(path)
        self.__upload_images(self.my_bucket)
        os.chdir(original_path)

    def remove_expired(self):
        '''
        get todays date
        connect to database
        create a table called expired_holidaysfrom all holidays dated today and earlier
        if the table existed insert said values into the table
        delete the values from the original database
        '''
        todays_date = datetime.date.today().strftime("%Y%m%d")
        with psycopg2.connect(host=c.HOST, user=c.USER, password=c.PASSWORD, dbname=c.DATABASE, port=c.PORT) as conn:
            with conn.cursor() as curs:
                curs.execute(f'''
                            CREATE TABLE IF NOT EXISTS expired_holidays AS
                                (SELECT * FROM hayes_holiday
                                WHERE next_date < '{todays_date}');
                            INSERT INTO expired_holidays
                                SELECT * FROM hayes_holiday
                                WHERE uuid NOT IN (SELECT uuid FROM expired_holidays)
                                AND hayes_holiday.next_date < '{todays_date}';
                            DELETE FROM hayes_holiday
                                WHERE hayes_holiday.next_date < '{todays_date}';                      
                            ''')

    def remove_duplicates(self):
        
        '''
        Use psycopg2 to run an SQL query to remove duplicates based off 4 variable columns.
        This is to try keep options available while not bloating the table with unnecessary duplicates.
        '''


        with psycopg2.connect(host=c.HOST, user=c.USER, password=c.PASSWORD, dbname=c.DATABASE, port=c.PORT) as conn:
            with conn.cursor() as curs:
                curs.execute('''
                CREATE TABLE distinct_store AS(
                    SELECT DISTINCT ON (url, price, group_size, next_date)
                    * 
                    FROM hayes_holiday);
                    DROP TABLE hayes_holiday;
                    ALTER TABLE distinct_store
                    RENAME TO hayes_holiday;
                ''')
