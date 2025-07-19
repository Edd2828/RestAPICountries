import pandas as pd

from .base import Base


class GetCountries(Base):
        def transform_data(self):
            df = pd.json_normalize(self.get_response())
            df = df[['name.common', 'name.official', 'population']]\
                .rename(columns={'name.common': 'common_name', 'name.official': 'official_name'})
            return df

class GetCountryCurrency(Base):
        def transform_data(self):
            data = self.get_response()

            flattened_data = []

            for country in data:
                for code, currency in country['currencies'].items():
                    flattened_data.append({
                        'country_name': country['name']['common'],
                        'currency_code': code
                    })

            df = pd.json_normalize(flattened_data)
            return df

class GetCountryLanguage(Base):
        def transform_data(self):
            data = self.get_response()

            flattened_data = []

            for country in data:
                for code, _ in country['languages'].items():
                    flattened_data.append({
                        'country_name': country['name']['common'],
                        'language_code': code,
                    })

            df = pd.json_normalize(flattened_data)
            return df

class GetCurrencies(Base):
        def transform_data(self):
            data = self.get_response()

            flattened_data = []

            for country in data:
                for code, currency in country['currencies'].items():
                    flattened_data.append({
                        'code': code,
                        'name': currency['name'],
                        'symbol': currency.get('symbol', '')
                    })

            df = pd.json_normalize(flattened_data)\
                .drop_duplicates()
            
            df = df.groupby('code', as_index=False).agg({'name': ', '.join, 'symbol': ', '.join})

            return df
        
class GetLanguages(Base):
        def transform_data(self):
            data = self.get_response()

            flattened_data = []

            for country in data:
                for code, language in country['languages'].items():
                    flattened_data.append({
                        'code': code,
                        'name': language,
                    })

            df = pd.json_normalize(flattened_data)\
                .drop_duplicates()

            df = df.groupby('code', as_index=False).agg({'name': ', '.join})

            return df

if __name__ == "__main__":
    pass  # This is just a placeholder to allow the module to be run directly for testing purposes.