import requests

import pandas as pd

from utils import base_url, base_storage_path


csv_name = 'countries.csv'
storage_path = base_storage_path() + csv_name
url = base_url(['name', 'population'])

# get country data
data = requests.get(url).json()

# normalize, rename, sort, and reset index
df = pd.json_normalize(data)
df = df[['name.common', 'name.official','population']]\
    .rename(columns={'name.common': 'common_name', 'name.official': 'official_name'})\
    .sort_values(by='common_name')\
    .reset_index(drop=True)

# set index to start from 1
df.index = df.index + 1

# save to csv
df.to_csv(storage_path, index_label='id')