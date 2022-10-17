
from setuptools import setup
from setuptools import find_packages

setup(
    name='hayes-travel-webscraper',
    version='0.0.1',
    description='Python package for scraping Hayes travelagents',
    url='https://github.com/CJohnston1994/2.WebScraper',
    author='Clark Johnston',
    license='MIT',
    packeges=find_packages(),
    install_requires=['selenium', ' psycopg2', 'boto3'],
)