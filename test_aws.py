import os, json, psycopg2, boto3, unittest
from aws import DataHandler
from sys import prefix
import pandas as pd
from sqlalchemy import create_engine

class AWSTestCase(unittest.TestCase):
    def setUp(self) -> None:
        data = json.load('tests/test/data.json')
        self.handler = DataHandler(data)
        return super().setUp()

    
    def test_process_data(self):
        '''
        test for process_data method
        '''
    
    def test_process_images(self):
        '''
        test for process_images method
        '''

    def test_images_already_scraped(self):
        '''
        test for images_already_scraped method
        '''