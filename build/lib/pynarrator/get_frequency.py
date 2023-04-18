import pandas as pd
import numpy as np

def get_frequency(df, date_field=None):
    """
    Get Date Frequency of the Data

    Function will group the data and estimate the frequency of the time stamps,
    returning 'year', 'quarter', 'month', 'week' or 'day'. You can use it on raw or aggregated data frames

    Args:
        df (pandas.DataFrame): Data frame of tibble, can be aggregated or raw
        date_field (str): Date field to be analyzed, by default the first date-like column will be used

    Returns:
        str: frequency - 'quarter', 'month', 'week' or 'day'

    Examples:
        >>> sales = read_data()
        >>> sales['Date'] = pd.to_datetime(sales['Date'])
        >>> sales_monthly = sales.groupby(['Region', pd.Grouper(key='Date', freq='MS')])['Sales'].sum().reset_index()
        >>> get_frequency(sales_monthly)
        
        >>> sales_weekly = sales.groupby(['Region', pd.Grouper(key='Date', freq=pd.offsets.Week(weekday=0))])['Sales'].sum().reset_index()
        >>> get_frequency(sales_weekly)
    """
    
    if not isinstance(df, pd.DataFrame):
        raise ValueError("'df' must be a pandas DataFrame")
        
    if len(df) == 0:
        raise ValueError("'df' must have at least 1 row")
        
    if date_field is None:
        date_fields = df.select_dtypes(include=[np.datetime64]).columns if not df.select_dtypes(include=[np.datetime64]).columns.empty else None
        
        if date_fields is None:
            raise ValueError("No date field detected in 'df'")
        elif len(date_fields) > 1:
            raise ValueError("Multiple date fields detected in 'df', please specify 'date_field'")
        else:
            date_field = date_fields[0]
    else:
        if date_field not in df.columns:
            raise ValueError("'date_field' must be present in the supplied data frame")
        elif not np.issubdtype(df[date_field].dtype, np.datetime64):
            raise ValueError("'date_field' must be of datetime type")
            
    df = df.rename(columns={date_field: "date_field"})
    
    est_frequency = df["date_field"].diff().dt.days.abs().value_counts().idxmax()
    
    if est_frequency > 300:
        frequency = "year"
    elif est_frequency > 35:
        frequency = "quarter"
    elif est_frequency > 8:
        frequency = "month"
    elif est_frequency > 3:
        frequency = "week"
    else:
        frequency = "day"
    
    return frequency


""" 
from pynarrator import read_data

sales = read_data()

sales['Date'] = pd.to_datetime(sales['Date'])

sales_monthly = sales.groupby(['Region', pd.Grouper(key='Date', freq='MS')])['Sales'].sum().reset_index()

sales_weekly = sales.groupby(['Region', pd.Grouper(key='Date', freq=pd.offsets.Week(weekday=0))])['Sales'].sum().reset_index()

freq_monthly = get_frequency(sales_monthly)
freq_weekly = get_frequency(sales_weekly)

print(f'Monthly time series identifies: {freq_monthly}')
print(f'Weekly time series identifies: {freq_weekly}') 
"""



