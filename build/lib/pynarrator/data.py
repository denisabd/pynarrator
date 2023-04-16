import pandas as pd

url = 'https://raw.githubusercontent.com/denisabd/pynarrator/main/data/sales.csv'

def read_data():
    return pd.read_csv(url, encoding='latin-1', keep_default_na=False)