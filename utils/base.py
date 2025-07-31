import requests
import psycopg2

import pandas as pd

from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

from .connection_details import get_connection_details


class PathLocations():
    BASE_PATH = Path().cwd()
    BASE_STORAGE_PATH = BASE_PATH / 'csv_exports'
    STAGING_SQL_FOLDER = BASE_PATH / 'sql' / 'staging'
    WAREHOUSE_SQL_FOLDER = BASE_PATH / 'sql' / 'warehouse'


class Base(ABC):

    BASE_STORAGE_PATH = PathLocations().BASE_STORAGE_PATH.as_posix() + '/'
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

    PATH_LOCATIONS = PathLocations()
    BASE_STORAGE_PATH = PATH_LOCATIONS.BASE_STORAGE_PATH.as_posix() + '/'
    STAGING_SQL_FOLDER = PATH_LOCATIONS.STAGING_SQL_FOLDER.as_posix() + '/'
    WAREHOUSE_SQL_FOLDER = PATH_LOCATIONS.WAREHOUSE_SQL_FOLDER.as_posix() + '/'

    connection_details = get_connection_details()

    HOST=connection_details['host']
    DATABASE=connection_details['database']
    USER=connection_details['user']
    PASSWORD=connection_details['password']

    def __init__(self, etl_stage, table_name: str | None=None):
        self.etl_stage = etl_stage
        self.table_name = table_name

    @classmethod
    def connect(cls):

        connection = psycopg2.connect(
            host=cls.HOST,
            database=cls.DATABASE,
            user=cls.USER,
            password=cls.PASSWORD
        )
        cursor = connection.cursor()

        return connection, cursor
    
    def staging_read_sql_file(self):
        file_path = self.STAGING_SQL_FOLDER + self.table_name + '.sql'
        with open(file_path, 'r') as file:
            sql_commands = file.read().replace('<csv_file_path>', self.BASE_STORAGE_PATH + self.table_name + '.csv')
        return sql_commands
    
    def warehouse_read_sql_file(self):
        file_path = self.WAREHOUSE_SQL_FOLDER + self.table_name + '.sql'
        with open(file_path, 'r') as file:
            sql_commands = file.read()
        return sql_commands
    
    def read_staging_clear_down(self):
        file_path = self.STAGING_SQL_FOLDER + 'clear_down.sql'
        with open(file_path, 'r') as file:
            sql_commands = file.read()
        return sql_commands

    def execute_sql(self, query=None):
        if not query:
            if self.etl_stage == 'staging':
                sql_query = self.staging_read_sql_file()
            elif self.etl_stage == 'warehouse':
                sql_query = self.warehouse_read_sql_file()
            else:
                raise ValueError("Invalid ETL stage specified. Use 'staging' or 'warehouse'.")
        else:
            sql_query = query

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
    pass