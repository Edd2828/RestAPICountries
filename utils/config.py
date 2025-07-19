from .get_data import (
    GetCountries, 
    GetCountryCurrency, 
    GetCountryLanguage, 
    GetCurrencies, 
    GetLanguages
    )


def get_etls_config():
    return [
        {'name': 'countries', 'class': GetCountries, 'sort_data': 'common_name', 'file_name': 'countries', 'filters': ['name', 'population']},
        {'name': 'country_currency', 'class': GetCountryCurrency,'sort_data': 'country_name', 'file_name': 'country_currency', 'filters': ['name', 'currencies']},
        {'name': 'country_language', 'class': GetCountryLanguage,'sort_data': 'country_name', 'file_name': 'country_language', 'filters': ['name', 'languages']},
        {'name': 'currencies', 'class': GetCurrencies,'sort_data': 'code', 'file_name': 'currencies', 'filters': 'currencies'},
        {'name': 'languages', 'class': GetLanguages,'sort_data': 'code', 'file_name': 'languages', 'filters': 'languages'},
    ]