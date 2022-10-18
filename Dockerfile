FROM python:3.10.4

ENV PASSWORD = envfile.PASSWORD
#
# installing chrome
RUN apt-get -y update \
    && apt-get install -y gnupg1 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get -y install libpq-dev gcc

#setting working directory
WORKDIR /hayes-travel-webscraper

#copying from main directory to container directory
COPY . .

#installing requirements
RUN pip install -r requirements.txt --no-cache-dir


#run the python file via commandline
CMD ["python", "webscraper/main.py"]