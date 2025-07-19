import requests
import psycopg2

from abc import ABC, abstractmethod
from typing import List

import pandas as pd


class Base(ABC):

    BASE_STORAGE_PATH = "C:/Edward/RestAPICountries/csv_exports/"
    BASE_URL = "https://restcountries.com/v3.1/all?fields="

    def __init__(self, sort_data, file_name, filters=str | List[str]):
        self.sort_data = sort_data
        self.file_name = file_name
        if isinstance(filters, str):
            self.base_url = self.BASE_URL + filters
        elif isinstance(filters, list):
            self.base_url = self.BASE_URL + ','.join(filters)
            
    def storage_location(self): 
        return self.BASE_STORAGE_PATH + self.file_name
    
    def get_response(self):
        """
        Fetches data from the REST API and returns it as a JSON object.
        """
        response = requests.get(self.base_url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    @abstractmethod
    def transform_data(self):
        return pd.DataFrame

    def save_to_csv(self):
        df = self.transform_data()\
            .sort_values(by=self.sort_data)\
            .reset_index(drop=True)
        df.index = df.index + 1
        df.to_csv(self.storage_location() + '.csv', index_label='id')


class PostgresBase():

    BASE_SQL_FOLDER = 'C:/Edward/RestAPICountries/sql/raw/'

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connect(self):

        connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        cursor = connection.cursor()

        return connection, cursor
    
    def read_sql_file(self, file_name):
        file_path = self.BASE_SQL_FOLDER + file_name + '.sql'
        with open(file_path, 'r') as file:
            sql_commands = file.read()
        return sql_commands
    
    def execute_sql(self, sql_query):
        connection, cursor = self.connect()
        try:
            cursor.execute(sql_query)
            connection.commit()  # Commit the changes to the database
        except Exception as e:
            print("Error while executing SQL", e)
        finally:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    pass  # This is just a placeholder to allow the module to be run directly for testing purposes.