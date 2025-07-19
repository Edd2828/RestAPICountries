from typing import List


def base_url(filters=str | List[str]) -> str:

    if isinstance(filters, str):
        filters = filters
    elif isinstance(filters, list):
        filters = ','.join(filters)
    elif not isinstance(filters, list | str):
        raise ValueError("filters must be a string or a list of strings")

    return f"https://restcountries.com/v3.1/all?fields={filters}"

def base_storage_path() -> str:
    return "C:/Edward/RestAPICountries/csv_exports/"



if __name__ == "__main__":
    print(base_url({'name', 'capital', 'currencies', 'languages', 'population', 'flag'}))