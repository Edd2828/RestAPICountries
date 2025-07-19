import requests

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



if __name__ == "__main__":
    class GetCountry(Base):
        def transform_data(self):
            df = pd.json_normalize(self.get_response())
            df = df[['name.common', 'name.official', 'population']]\
                .rename(columns={'name.common': 'common_name', 'name.official': 'official_name'})\
                .sort_values(by='common_name')\
                .reset_index(drop=True)
            df.index = df.index + 1
            return df
    extract = GetCountry(file_name='countries.csv', filters=['name', 'population'])
    extract.save_to_csv()

if __name__ == "__main__":
    pass  # This is just a placeholder to allow the module to be run directly for testing purposes.