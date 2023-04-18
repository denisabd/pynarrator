import pandas as pd
import numpy as np
import datetime as dt
from typing import Optional

from pynarrator import get_frequency


def get_py_date(df: pd.DataFrame, frequency: Optional[str] = None):
    """
    Calculate the prior year date based on the maximum date in the DataFrame and the given frequency.

    Parameters
    ----------
    df : pd.DataFrame
        Input pandas DataFrame containing the data to be analyzed, with a date column.
    frequency : str, optional
        Date frequency to use for the calculation, by default None.
        If not provided, the frequency will be inferred from the DataFrame.

    Examples
    --------
    >>> data = {'Monthly Date': pd.date_range(start='2021-01-01', periods=15, freq='MS'),
        'Value': [10, 15, 20, 25, 30, 10, 15, 20, 25, 30, 10, 15, 20, 25, 30],
        'Category': ['A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A']}
    >>> df = pd.DataFrame(data)
    >>> get_py_date(df)    

    Returns
    -------
    dt.date
        A date object representing the prior year date.
    """
    # Table must be a pandas DataFrame and have at least one row
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df must be a pandas DataFrame")
    if df.shape[0] == 0:
        raise ValueError("df must have at least one row, execution is stopped")
    
    date_field = df.select_dtypes(include=[np.datetime64]).columns[0] if not df.select_dtypes(include=[np.datetime64]).columns.empty else None
    
    if date_field is None:
        raise ValueError("Data frame must contain one date column")

    # Calculating frequency if not available
    if frequency is None:
        frequency = get_frequency(df)

    max_date = df[date_field].max()
    max_year = max_date.year

    if frequency == "week":
        df_weekly = (
            df[[date_field]]
            .drop_duplicates()
            .sort_values(by=date_field)
            .assign(week=lambda x: x[date_field].dt.isocalendar().week,
                    year=lambda x: x[date_field].dt.year)
        )

        max_week = df_weekly.loc[df_weekly[date_field] == max_date, "week"].iat[0]

        py_date = df_weekly.loc[(df_weekly["year"] == max_year - 1) & (df_weekly["week"] == max_week), date_field].values
        py_date = pd.to_datetime(py_date)

        if len(py_date) == 0:
            py_date = max_date - pd.DateOffset(years=1)
        else:
            py_date = py_date[0]
    else:
        py_date = max_date - pd.DateOffset(years=1)

    return py_date.date()


def ytd_volume(
        df, 
        measure = None, 
        date = None, 
        summarization = "sum", 
        current_year = None, 
        cy_date = None):
    """
    Calculate the year-to-date (YTD) volume of a given measure in a pandas DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input pandas DataFrame containing the data to be analyzed.
    measure : str, optional
        Column name of the measure to calculate the YTD volume for, by default None.
        If not provided, the first numerical column in the DataFrame will be used.
    date : str, optional
        Column name of the date to use for the YTD calculation, by default None.
        If not provided, the first datetime column in the DataFrame will be used.
    summarization : str, optional
        Summarization method to use for calculating YTD volume, by default "sum".
        Must be one of {"sum", "count", "average"}.
    current_year : int, optional
        Year to use for the YTD calculation, by default None.
        If not provided, the current year will be used.
    cy_date : datetime, optional
        Date to use for the YTD calculation, by default None.
        If not provided, the current date will be used.

    Raises
    ------
    ValueError
        If `df` is not a pandas DataFrame or has no rows.
        If `summarization` is not one of {"sum", "count", "average"}.
        If `measure` or `date` is not a valid column in the DataFrame.
        If `date` is not a valid datetime column in the DataFrame.

    Examples
    --------
    >>> data = {'Monthly Date': pd.date_range(start='2021-01-01', periods=15, freq='MS'),
        'Value': [10, 15, 20, 25, 30, 10, 15, 20, 25, 30, 10, 15, 20, 25, 30],
        'Category': ['A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A']}
    >>> df = pd.DataFrame(data)
    >>> ytd_volume(df)

    Returns
    -------
    pd.DataFrame
        A new pandas DataFrame with the YTD volume calculated for each row.
    """
    # Table must be a pandas DataFrame and have at least one row
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df must be a pandas DataFrame")
    if df.shape[0] == 0:
        raise ValueError("df must have at least one row, execution is stopped")
  
    # Summarization Assertion
    if summarization not in ["sum", "count", "average"]:
        raise ValueError("summarization must of be one of: 'sum', 'count' or 'mean'.")
  
    # Measure, Date and Dimensions Assertion
    if measure is not None:
        if measure not in df.columns:
            raise ValueError("measure must a column in the dataset")
    else:
        # If measure isn't supplied get the first numerical column from it
        measure = df.select_dtypes(include=[np.number]).columns[0]
  
    # Get Date
    if date is not None:
        if date not in df.columns:
            raise ValueError("date must a column in the dataset")
  
        df[date] = pd.to_datetime(df[date])
  
        if not pd.api.types.is_datetime64_any_dtype(df[date]):
            raise ValueError("'date' must be a date column in the dataset")
    else:
        # Getting the first date field available
        date = df.select_dtypes(include=[np.datetime64]).columns[0] if not df.select_dtypes(include=[np.datetime64]).columns.empty else None
        
        if date is None:
            raise ValueError("No date column found in the dataset")

    # Current Year's Date
    if cy_date is None:
        cy_date = df[date].max()
    else:
        cy_date = pd.to_datetime(cy_date)
  
    # Current year assertion
    if current_year is not None and current_year != cy_date.year:
        try:
            current_year = int(current_year)
        except:
            raise ValueError("current_year argument must be numeric or convertable to numeric like 2022 or '2022' ")
    else:
        current_year = cy_date.year

    cy_volume = (df.assign(year=df[date].dt.year)
                .query('year == @current_year and `{0}` <= @cy_date'.format(date))
                .agg({measure: summarization})
                .squeeze()
                )
  
    return cy_volume

def pytd_volume(
        df, 
        measure = None, 
        date = None, 
        summarization = "sum", 
        current_year = None, 
        py_date = None):
    """
    Calculate the previous year-to-date (PYTD) volume of a given measure in a pandas DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input pandas DataFrame containing the data to be analyzed.
    measure : str, optional
        Column name of the measure to calculate the YTD volume for, by default None.
        If not provided, the first numerical column in the DataFrame will be used.
    date : str, optional
        Column name of the date to use for the YTD calculation, by default None.
        If not provided, the first datetime column in the DataFrame will be used.
    summarization : str, optional
        Summarization method to use for calculating YTD volume, by default "sum".
        Must be one of {"sum", "count", "average"}.
    current_year : int, optional
        Year to use for the YTD calculation, by default None.
        If not provided, the current year will be used.
    py_date : datetime, optional
        Date to use for the YTD calculation, by default None.
        If not provided, the current date will be used.

    Raises
    ------
    ValueError
        If `df` is not a pandas DataFrame or has no rows.
        If `summarization` is not one of {"sum", "count", "average"}.
        If `measure` or `date` is not a valid column in the DataFrame.
        If `date` is not a valid datetime column in the DataFrame.

    Examples
    --------
    >>> data = {'Monthly Date': pd.date_range(start='2021-01-01', periods=15, freq='MS'),
        'Value': [10, 15, 20, 25, 30, 10, 15, 20, 25, 30, 10, 15, 20, 25, 30],
        'Category': ['A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A']}
    >>> df = pd.DataFrame(data)
    >>> pytd_volume(df)

    Returns
    -------
    pd.DataFrame
        A new pandas DataFrame with the YTD volume calculated for each row.
    """
    # Table must be a pandas DataFrame and have at least one row
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df must be a pandas DataFrame")
    if df.shape[0] == 0:
        raise ValueError("df must have at least one row, execution is stopped")
  
    # Summarization Assertion
    if summarization not in ["sum", "count", "average"]:
        raise ValueError("summarization must of be one of: 'sum', 'count' or 'mean'.")
  
    # Measure, Date and Dimensions Assertion
    if measure is not None:
        if measure not in df.columns:
            raise ValueError("measure must a column in the dataset")
    else:
        # If measure isn't supplied get the first numerical column from it
        measure = df.select_dtypes(include=[np.number]).columns[0]
  
    # Get Date
    if date is not None:
        if date not in df.columns:
            raise ValueError("date must a column in the dataset")
  
        df[date] = pd.to_datetime(df[date])
    
        if not pd.api.types.is_datetime64_any_dtype(df[date]):
            raise ValueError("'date' must be a date column in the dataset")
    else:
        # Getting the first date field available
        date = df.select_dtypes(include=[np.datetime64]).columns[0] if not df.select_dtypes(include=[np.datetime64]).columns.empty else None
        
        if date is None:
            raise ValueError("No date column found in the dataset")

    # Current Year's Date
    if py_date is None:
        py_date = get_py_date(df)
    else:
        py_date = pd.to_datetime(py_date)
  
    # Current year assertion
    if current_year is not None and current_year - 1 != py_date.year:
        try:
            current_year = int(current_year)
        except:
            raise ValueError("current_year argument must be numeric or convertable to numeric like 2022 or '2022' ")
    else:
        previous_year = py_date.year

    py_volume = (df.assign(year=df[date].dt.year)
                .query('year == @previous_year and `{0}` <= @py_date'.format(date))
                .agg({measure: summarization})
                .squeeze()
                )
  
    return py_volume

"""
data = {'Monthly Date': pd.date_range(start='2021-01-01', periods=15, freq='MS'),
        'Value': [10, 15, 20, 25, 30, 10, 15, 20, 25, 30, 10, 15, 20, 25, 30],
        'Category': ['A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A']}

df = pd.DataFrame(data)

py = get_py_date(df)
ytd = ytd_volume(df, measure = 'Value')
pytd = pytd_volume(df, measure = 'Value')

print(py)
print(ytd)
print(pytd)
"""