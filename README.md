---
noteId: "b57effa0f73111ec8f3c130c8c0b6fb0"
tags: []

---

TO BE COMPLETED

# Hayes Travel Webscraper
> This project is to create a webscraper to accurately asses relevant holiday deals with Hayes Travel, a UK based travel agent


## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
- This is a webscraper to collect holiday data from Hays Travel using selenium to scrape from the destinations page of the Hayes travel website. This data is then cleaned  using pandas and send to an AWS Relational database using Pandas and SQLAlchemy. The data is then sent to an s3 bucket using boto3 and Finally Psycopg2 is used to issue SQL queries to the database in order to clean outdated entries and remove duplicates. This functionality was then containerized and uploaded to Docker hub.
- Git hub actions is used to implement CI/CD functionality to allow streamline development and updating via gitHub pushes.

- This project was undertaken to track holiday prices of a specific travel agent. Allowing for further analysis on trends, popularity/price ratios and price comparisons depending on the time of year. All historic data is collected in a seperate table to allow for comparisons. 

- I choose this project to gain skills and knowledge to work towards a career in Data engineering, therefore this is a self-imporvement project. 
<!-- You don't have to answer all the questions - just the ones relevant to your project. -->


## Technologies Used
- Python
  - Selenium
  - Boto3
  - Psycopg2
  -Pandas
  -SQLAlchemy
- PostgreSQL
- Amazon Web Services
  -S3
  -RDS
  -EC2 - TODO
- GitHub Actions



## Features
List the ready features here:
- Automatic scraping in a precise and effective manner
- Automatic database cleaning, removes duplicates
- Collects expired entries for future analysis
- files saved locally then removed after scraper completion to reduce memory usage

## Setup
- Dockerhub - https://hub.docker.com/r/theglink/hayes-travel-webscraper
  -environment variables required:

  '-S3_ACCESS_KEY
  -S3_SECRET_KEY
  -BUCKET_NAME
  -HOST
  -PASSWORD
  -DB_USER
  -DATABASE_NAME
  -PORT'
- Requirements.txt found in root directory
  -boto3==1.24.22
  -pandas==1.4.3
  -psycopg2==2.9.3
  -psycopg2_binary==2.9.3
  -selenium==4.4.0
  -SQLAlchemy==1.4.39
  -webdriver_manager==3.7.0


## Usage
Usage is very simple, Simply run the docker container providing the environment file using
'docker run --env-file env-file.env hayes_travel_scraper'
wher the environment file is laid out as shown above. Database api is locked to psycopg2 and databasetype is locked to postgresql

## Project Status
Project is: _in progress_ 

## Room for Improvement

Room for improvement:
- Add more error checking to the scraper. Some variance in the website lead to selenium not finding elements and leaving some null values
- Improve and add more intricate RDS functionality.
- allow other database APIs and types to be used.

To do:
- Change data cleaning to be mainly done in pandas
- Create EC2 instance and add monitoring and metrics with Prometheus and Grafana


## Acknowledgements
Give credit here.
- This project was inspired by AICore
- This project was based on [this tutorial](https://www.example.com).
- Many thanks to Harry Berg, Blair Martin and Wayne Rose


## Contact
gitHub      - https://github.com/CJohnston1994
linkedin    - https://www.linkedin.com/in/clark-johnston-203905116/

## License
MIT License

Copyright (c) 2022 Clark Johnston

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This project is open source and available under the [MIT License]().

<!-- Optional -->

<!-- You don't have to include all sections - just the one's relevant to your project -->
