from bs4 import BeautifulSoup
import pandas as pd

class ParserService:
    @staticmethod
    def create_df_worldometer(raw_data):
        """
        Parses the raw HTML response from Worldometer and returns a DataFrame from it

        @Params:
        raw_data (string): request.text from Worldometer

        @Returns:
        DataFrame
        """
        soup = BeautifulSoup(raw_data, features="html.parser")

        COLUMNS = ["Country", "Total Cases", "New Cases", "Total Deaths", "New Deaths", "Active Cases", "Recovered", "Critical"]

        _id = "main_table_countries"

        countries_data = soup.find("table", attrs={"id": _id}).find("tbody").findAll("tr")

        parsed_data = []

        for country in countries_data:
            parsed_data.append([data.get_text() for data in country.findAll("td")])

        return pd.DataFrame(parsed_data, columns=COLUMNS)

    @staticmethod
    def parse_last_updated(raw_data):
        """
        Parses the raw HTML response from Worldometer and returns the lastest update time from the webpage

        @Params:
        raw_data (string): request.text from Worldometer

        @Returns:
        Last updated time (string)
        """

        soup = BeautifulSoup(raw_data, features="html.parser")

        last_updated = soup.find("div", {"style": "font-size:13px; color:#999; text-align:center"})
        
        return last_updated.text