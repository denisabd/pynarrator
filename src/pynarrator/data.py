import pandas as pd

def read_data():
    return pd.read_csv('data/sales.csv', encoding='latin-1', keep_default_na=False)
