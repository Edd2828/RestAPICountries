import requests

import pandas as pd

from utils import base_url, base_storage_path


csv_name = 'currencies.csv'
storage_path = base_storage_path() + csv_name
url = base_url('currencies')

# get country data
data = requests.get(url).json()

flattened_data = []

for country in data:
    for code, currency in country['currencies'].items():
        flattened_data.append({
            'code': code,
            'name': currency['name'],
            'symbol': currency.get('symbol', '')
        })

# normalize, rename, sort, and reset index
df = pd.json_normalize(flattened_data)\
    .drop_duplicates()\
    .sort_values(by='code')\
    .reset_index(drop=True)

# set index to start from 1
df.index = df.index + 1

# save to csv
df.to_csv(storage_path, index_label='id')