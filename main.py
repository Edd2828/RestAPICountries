import concurrent.futures

from utils.get_data import (
    GetCountries, 
    GetCountryCurrency, 
    GetCountryLanguage, 
    GetCurrencies, 
    GetLanguages
    )


etls_config = [
    {'name': 'countries', 'class': GetCountries, 'sort_data': 'common_name', 'file_name': 'countries', 'filters': ['name', 'population']},
    {'name': 'country_currency', 'class': GetCountryCurrency,'sort_data': 'country_name', 'file_name': 'country_currency', 'filters': ['name', 'currencies']},
    {'name': 'country_language', 'class': GetCountryLanguage,'sort_data': 'country_name', 'file_name': 'country_language', 'filters': ['name', 'languages']},
    {'name': 'currencies', 'class': GetCurrencies,'sort_data': 'code', 'file_name': 'currencies', 'filters': 'currencies'},
    {'name': 'languages', 'class': GetLanguages,'sort_data': 'code', 'file_name': 'languages', 'filters': 'languages'},
]

def create_extractor(class_name, sort_data, file_name, filters):
    return class_name(sort_data=sort_data, file_name=file_name, filters=filters)

def run_extraction(extractor):
    extractor.save_to_csv()

# Create instances for each extractor
countries_extractor = GetCountries(sort_data='common_name', file_name='countries', filters=['name', 'population'])
currency_extractor = GetCountryCurrency(sort_data='country_name', file_name='country_currency', filters=['name', 'currencies'])

# Execute in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(run_extraction, create_extractor(etl['class'], etl['sort_data'], etl['file_name'], etl['filters'])) for etl in etls_config]
    
    # Wait for all futures to complete
    for future in concurrent.futures.as_completed(futures):
        future.result()  # This will raise any exceptions that occurred

print("All extractions completed.")