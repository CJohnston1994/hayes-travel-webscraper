import boto3
import os

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

