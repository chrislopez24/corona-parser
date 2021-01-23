from bs4 import BeautifulSoup
import pandas as pd
import re

class ParserService:

    @staticmethod
    def format_table_header_column(th):
        """
        Parses a raw HTML table header column and returns formatted string

        @Params:
        th (string): TableHeader column from countries table

        @Returns:
        Table header as string
        """

        header = " ".join(th.strings)  # join strings broken by <br> tags
        # replace non-breaking space with space and remove \n
        header = header.replace(u"\xa0", u" ").replace("\n", "") 
        return header.replace(", ", "/")

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

        _id = "main_table_countries_today"

        countries_table = soup.find("table", attrs={"id": _id})

        columns = [ParserService.format_table_header_column(th) for th
                   in countries_table.find("thead").findAll("th")]
   
        #vars
        parsed_data = []
        regx = r'(\n|\+|,)'
        country_rows = countries_table.find("tbody").find_all("tr")

        #utility functions
        def sort_alphabetically(element):
            sorted_element = element.findAll("td")[1].get_text().strip()
            return sorted_element
        
        #sort countries
        country_rows.sort(key=sort_alphabetically)

        for country_row in country_rows:
            country_classname = re.sub(regx, "", country_row.findAll("td")[1].get_text())
            #Filter unnecesary data, gather countries, continents and World results
            if country_classname == '' or 0:
                continue
            parsed_data.append([data.get_text().strip() for data
                                in country_row.findAll("td")])
        
        #Prepare the data to add new columns and manipulate data
        df_parsed = pd.DataFrame(parsed_data, columns=columns).replace(to_replace=[""], value=0)
        df = df_parsed.apply(lambda x: x.str.replace(',',''))

        #Create new Percentage collumns using float values
        df['Death Percentage'] = (
           df['Total Deaths'].astype(float) / df['Total Cases'].astype(float) * 100
        )
        df['Population Test Percentage'] = (
            df['Total Tests'].astype(float) / df['Population'].astype(float) * 100
        )

        #Round the big float number to 3 decimal digits and bring it back to String type
        df['Death Percentage'] = df['Death Percentage'].round(3).fillna(0).astype(str)
        df['Population Test Percentage'] = df['Population Test Percentage'].round(3).fillna(0).astype(str)

        return df.replace(to_replace=[None], value=0)

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
        
        _styles = "font-size:13px; color:#999; margin-top:5px; text-align:center"
        
        last_updated = soup.find("div", {"style": _styles})
        
        return last_updated.text
