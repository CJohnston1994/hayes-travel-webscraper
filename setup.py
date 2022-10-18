import os
from setuptools import setup
from setuptools import find_packages
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='hayes-travel-webscraper',
    version='0.0.1',
    description='Python package for scraping Hayes travelagents',
    url='https://github.com/CJohnston1994/2.WebScraper',
    author='Clark Johnston',
    license='MIT',
    packeges=find_packages(['boto3','pandas','psycopg2-binary','selenium','webdriver_manager','sqlalchemy'])   
)


