import json, unittest, boto3
from unittest import main, TestCase
from unittest.mock import Mock
from botocore.stub import Stubber
from webscraper.utils.aws import DataHandler
from sqlalchemy import create_engine

class AWSTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.load('tests/test/data.json')
        self.client = boto3.client('s3')
        self.handler = DataHandler()
        self.mock = Mock()
        return super().setUp()

    def test_process_data(self, mock_check_data):
        '''
        test for process_data method
        '''
        self.handler.process_data()

    
    def test_process_images(self):
        '''
        test for process_images method
        '''

    def test_images_already_scraped(self):
        '''
        test for images_already_scraped method
        '''