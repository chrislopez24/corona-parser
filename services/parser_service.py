from bs4 import BeautifulSoup
import pandas as pd

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

        header_string = " ".join(th.strings)  # join strings broken by <br> tags
        return header_string.replace(u"\xa0", u" ")  # replace non-breaking space with space

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

        parsed_data = []

        country_rows = countries_table.find("tbody").find_all("tr")

        for country_row in country_rows:
            parsed_data.append([data.get_text().replace("\n", "") for data
                                in country_row.findAll("td")])

        df = pd.DataFrame(parsed_data, columns=columns)
        return df.replace(to_replace=[""], value=0)

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
