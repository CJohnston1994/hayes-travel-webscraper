---
noteId: "b57effa0f73111ec8f3c130c8c0b6fb0"
tags: []

---

TO BE COMPLETED

# Project Name
> This is a webscraper to collect holiday data from Hays Travel using selenium.
> The data is then cleaned and converted into a pandas dataframe
> In a clean database the table is generated using the pandas to_sql function.
> Finally the database is maintained using psycopg2 to run sql queries to clear Expired

> Git hub actions is used to implement CI/CD functionality to build 


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
- Provide general information about your project here.
- What problem does it (intend to) solve?
- What is the purpose of your project?
- Why did you undertake it?
<!-- You don't have to answer all the questions - just the ones relevant to your project. -->


## Technologies Used
- Python
  - Selenium
  - Boto3
  - Psycopg2

- Amazon Web Services
  -S3
  -RDS
  -EC2
- GitHub Actions


## Features
List the ready features here:
- Automatic database cleaning, removes duplicates and expired deals
- 


## UML
![Example screenshot](.img/UML Diagram Data Collection.jpg)
<!-- If you have screenshots you'd like to share, include them here. -->


## Setup
What are the project requirements/dependencies? Where are they listed? A requirements.txt or a Pipfile.lock file perhaps? Where is it located?
Proceed to describe how to install / setup one's local environment / get started with the project.


## Usage
How does one go about using it?
Provide various use cases and code examples here.

`write-your-code-here`


## Project Status
Project is: _in progress_ 

## Room for Improvement

Room for improvement:
- Add more error checking to the scraper. Some variance in the website lead to selenium not finding elements and leaving some null values
- Improve and add more intricate RDS functionality.

To do:
- Change data cleaning to be mainly done in pandas
- Create EC2 instance and add monitoring and metrics with Prometheus and Grafana


## Acknowledgements
Give credit here.
- This project was inspired by AICore
- This project was based on [this tutorial](https://www.example.com).
- Many thanks to Harry Berg, Blair Martin and Wayne Rose


## Contact
Created by [@flynerdpl](https://www.flynerd.pl/) - feel free to contact me!


<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->
