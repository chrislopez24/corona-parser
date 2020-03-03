from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

web = requests.get('https://www.worldometers.info/coronavirus/#countries')

soup = BeautifulSoup(web.text, features="html.parser")

_id = "main_table_countries"

raw_data = soup.find("table", attrs={"id": _id}).find("tbody").findAll("tr")

parsed_data = []

for country in raw_data:
  parsed_data.append([data.get_text() for data in country.findAll("td")])

COLUMNS = ["Country", "Total Cases", "New Cases", "Total Deaths", "New Deaths", "Active Cases", "Recovered", "Critical"]

#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

output = pd.DataFrame(parsed_data, columns=COLUMNS)

output.to_csv(r'./cases.csv', index = False)
print(output.to_string)
