import json, unittest
from unittest import main, TestCase
from unittest.mock import mock
from aws import DataHandler
from sys import prefix
import pandas as pd
from sqlalchemy import create_engine

class AWSTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.load('tests/test/data.json')
        self.handler = DataHandler()
        return super().setUp()

    @mock.patch('2.WEBSCRAPER.aws.DataHandler')
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