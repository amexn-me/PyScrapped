#Importing required packages
#--For Web Scarping
from bs4 import BeautifulSoup
import requests

#-- For Database Management
from sqlalchemy import create_engine
import psycopg2

#-- For Controlling Data
import pandas as pd

#Inserting the URL of Website/Websites that we want to scrape
#--When scraping from a single website,then load its URL it into a string:
url='URL_OF_WEBSITE'
#--When scraping from multiple websites, then load their URLs into an array:
urls= [
'URL_OF_WEBSITE1',
'URL_OF_WEBSITE2',
'URL_OF_WEBSITE3'
]

#loading empty array for incoming data
scrapped_data =[]

#Scraping when there is only one targeted webste
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")
#--identify the HTML Element that we want to scrape (Here, we are scraping from a Table Element)
sample_table = soup.find('table', {"class" : "TableClassName"})
#--In order to skip spaces with no data, we use "try" exception
try:
    #Now we will loop inside the scrapped Table Element to load those data into pre-built arrays
    for table_row in sample_table.find_all('tr'):
        table_cols = table_row.find_all('td')
        if len(table_cols) == 5: #Now, we will verify the data by comparing actuals with scrapped. Here, by comparing the number of columns scraped from the targeted Table Element with it's actual.
            #Strip only text from the data available.
            scrapped_data.append((table_cols[0].text.strip(), table_cols[1].text.strip(), table_cols[2].text.strip(), table_cols[2].text.strip(), table_cols[4].text.strip()))
except: pass  


#Scraping when there are multiple targeted webste
for u in urls:
    html = requests.get(u).text
    soup = BeautifulSoup(html, "html.parser")
    #--identify the HTML Element that we want to scrape (Here, we are scraping from a Table Element)
    sample_table = soup.find('table', {"class" : "TableClassName"})
    #--In order to skip spaces with no data, we use "try" exception
    try:
        #Now we will loop inside the scrapped Table Element to load those data into pre-built arrays
        for table_row in sample_table.find_all('tr'):
            table_cols = table_row.find_all('td')
            if len(table_cols) == 5: #Now, we will verify the data by comparing actuals with scrapped. Here, by comparing the number of columns scraped from the targeted Table Element with it's actual.
                #Strip only text from the data available.
                scrapped_data.append((table_cols[0].text.strip(), table_cols[1].text.strip(), table_cols[2].text.strip(), table_cols[2].text.strip(), table_cols[4].text.strip()))
    except: pass  

#convert the array into a dataframe using pandas
df = pd.DataFrame(scrapped_data)

#To rename the column headings
df.columns = ['ColHead1', 'ColHead2', 'ColHead3','ColHead4', 'ColHead5']

#To save these scrapped data into PostgreSQL
engine = create_engine('postgresql://username:password@psqladdress:port/DBName')
df.to_sql('nameoftable', engine, if_exists='append')