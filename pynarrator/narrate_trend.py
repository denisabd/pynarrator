import pandas as pd
from pynarrator import ytd_volume, pytd_volume

def get_trend_outliers(
    df, 
    dimension, 
    measure, 
    total=None, 
    summarization="sum", 
    coverage=0.5, 
    coverage_limit=5):
    """
    Returns trend outliers based on a given dataframe, dimension, and measure.

    Args:
    df (pandas.DataFrame): The dataframe to analyze.
    dimension (str): The dimension to group by.
    measure (str): The measure to use for aggregation.
    total (float, optional): The total value to use for calculation. Defaults to None.
    summarization (str, optional): The type of summarization to use (sum, count, or average). Defaults to "sum".
    coverage (float, optional): The coverage percentage to use for filtering. Defaults to 0.5.
    coverage_limit (int, optional): The maximum number of outliers to return. Defaults to 5.

    Returns:
    dict: A dictionary containing the number of outliers, outlier levels, outlier values, and outlier percentages.

    Raises:
    ValueError: If the summarization parameter is not one of "sum", "count", or "average".

    Examples:
    >>> import pandas as pd
    >>> sales = read_data()
    >>> sales['Date'] = pd.to_datetime(sales['Date'])
    >>> sales_monthly = sales.groupby(['Region', 'Product', pd.Grouper(key='Date', freq='MS')])['Sales'].sum().reset_index()
    >>> get_trend_outliers(sales_monthly)
    {'n_outliers': 3, 'outlier_levels': ['qux', 'baz', 'bar'], 'outlier_values': [80, 60, 40], 'outlier_values_p': ['25.0%', '18.75%', '12.5%']}

    >>> get_trend_outliers(sales_monthly, 'A', 'C', summarization='average')
    {'n_outliers': 3, 'outlier_levels': ['qux', 'baz', 'bar'], 'outlier_values': [1.0, -0.25, -0.5], 'outlier_values_p': ['47.62%', '11.90%', '23.81%']}
    """
    if summarization in ["sum", "count"]:
        if total is None:
            total = table[measure].sum().round(2)
      
        grouped = df.groupby(dimension)

        # Define a function to apply to each group
        def process_group(group, ytd_volume, pytd_volume, summarization, measure):
            curr_volume = ytd_volume(group, summarization=summarization, measure=measure)
            prev_volume = pytd_volume(group, summarization=summarization, measure=measure)
            change = curr_volume - prev_volume
            change_p = f"{round(change / prev_volume * 100, 2)}%"
            abs_change = abs(change)
            trend = "increase" if change > 0 else "decrease"
            
            output = pd.Series({
                "curr_volume": curr_volume,
                "prev_volume": prev_volume,
                "change": change,
                "change_p": change_p,
                "abs_change": abs_change,
                "trend": trend,
            })
            
            return output

        # Apply the function to each group and create a new DataFrame
        table = grouped.apply(process_group, ytd_volume, pytd_volume, summarization, measure)

        # Reset the index and sort by abs_change
        table = table.reset_index().sort_values(by="abs_change", ascending=False)

        # Assuming you have a DataFrame named 'table'
        #table['share'] = table['abs_change'] / table['abs_change'].sum()
        #table['cum_share'] = table['share'].cumsum()
        #table['lag_cum_share'] = table['cum_share'].shift(fill_value=False)

        table = (
            table.assign(share=lambda x: x['abs_change'] / x['abs_change'].sum())
                  .assign(cum_share=lambda x: x['share'].cumsum())
                  .assign(lag_cum_share=lambda x: x['cum_share'].shift(fill_value=False))
        )

        table = table[table['lag_cum_share'] < coverage]
        table = table.head(coverage_limit)

        if len(table) == 1 and table['cum_share'].iloc[0] == 1:
            return None

    elif summarization == 'average':
        if total is None:
            total = table[measure].mean().round(2)

        table = (table
          .assign(share = lambda x: x[measure]/total - 1)
          .assign(abs_share=lambda x: x['share'].abs())
          .sort_values(by='abs_share', ascending=False)
          .assign(cum_share=lambda x: x['share'].abs().cumsum()/(x['share'].max() - x['share'].min()))
          .loc[lambda x: (x['cum_share'] >= coverage*2).shift(fill_value=False).cumsum() == 0]
          .iloc[:coverage_limit]
          )

    n_outliers = table.shape[0]
    outlier_levels = table[dimension].astype(str).values.tolist()
    outlier_values = table[measure].round(1).values.tolist()
    outlier_values_p = (table["share"].round(2) * 100).astype(str).add("%").values.tolist()

    output = {
        "n_outliers": n_outliers,
        "outlier_levels": outlier_levels,
        "outlier_values": outlier_values,
        "outlier_values_p": outlier_values_p
    }

    return output

def narrate_trend(
  df,
  measure = None,
  dimensions = None,
  summarization = 'sum',
  coverage = 0.5,
  coverage_limit = 5,
  narration_depth = 2,
  template_total = "From {timeframe_prev} to {timeframe_curr}, {measure} had an {trend} of {change} ({change_p}, {total_prev} to {total_curr}).",
  template_average = "Average {measure} had an {trend} of {change} ({change_p}, {total_prev} to {total_curr}).",
  template_outlier = "{dimension} with biggest changes of {measure} is {outlier_insight}.",
  template_outlier_multiple = "{pluralize(dimension)} with biggest changes of {measure} are {outlier_insight}.",
  template_outlier_l2 = "In {level_l1}, significant {level_l2} by {measure} change is {outlier_insight}.",
  template_outlier_l2_multiple = "In {level_l1}, significant {pluralize(level_l2)} by {measure} change are {outlier_insight}.",
  return_data = False,
  simplify = False
  ):
  """
  This function generates a narrative report based on a given data frame and parameters.
  
  Parameters:
  -----------
  df : pandas.DataFrame
      The data frame containing the data to analyze.
  measure : str or None
      The name of the numeric variable to analyze. If None, the first numeric field
      available in the data frame will be used.
  dimensions : list or None
      The names of the categorical variables to include in the analysis. If None, all
      character or factor variables in the data frame will be used.
  summarization : str, {'sum', 'count', 'average'}
      The method to use for summarizing the data. Default is 'sum'.
  coverage : float, optional
      The portion of variability to be covered by the narrative, expressed as a value
      between 0 and 1. Default is 0.5.
  coverage_limit : int, optional
      The maximum number of elements to be narrated. If the number of elements is greater
      than this value, the narrative will be truncated. Default is 5.
  narration_depth : int, {1, 2}
      The depth of the analysis to include in the narrative. 1 for summary and 2 for detailed.
  template_total : str
      The template to use for the narrative report on total volumes.
  template_average : str
      The template to use for the narrative report on average volumes.
  template_outlier : str
      The template to use for the narrative report on single outliers.
  template_outlier_multiple : str
      The template to use for the narrative report on multiple outliers.
  template_outlier_l2 : str
      The template to use for the narrative report on hierarchical single outliers.
  template_outlier_l2_multiple : str
      The template to use for the narrative report on hierarchical multiple outliers.
  return_data : bool, optional
      If True, the function will return a dictionary containing the variables used in the
      function's templates. Default is False.
  simplify : bool, optional
      If True, the function will return a list of the narrative strings instead of a
      dictionary. Default is False.
      
  Returns:
  --------
  narrative : dict or list
      The narrative report generated by the function. If simplify is True, a list of the
      narrative strings will be returned instead of a dictionary.

  Example:
    from pynarrator import *\
    narrative = narrate_trend(df, measure = 'Sales', dimensions = ['Region', 'Product'])
  """
  # Assert data frame
  if not isinstance(df, pd.DataFrame):
    print('df must be a pandas DataFrame')
    return
  
  if isinstance(measure, type(None)):
    measure = df.\
      select_dtypes(include = 'number').\
      columns[0]
    
  if isinstance(dimensions, type(None)):
    dimensions = df.\
      select_dtypes(include = ['object', 'category']).\
      columns.\
      values.\
      tolist()
      
  dimension_one = dimensions[0]
  
  if summarization == 'sum':
    total_raw = df[measure].sum().round(2)
  elif summarization == 'average':
    total_raw = df[measure].mean().round(2)
  elif summarization == 'count':
    total_raw = df[measure].count()

  total = total_raw
  
  narrative_total = eval(f"f'{template_total}'")
  
  narrative = {
    f'Total {measure}': narrative_total
  } 
   
  variables = {
      f'Total {measure}': {
        'narrative_total': narrative_total,
        'template_total': template_total,
        'measure': measure,
        'dimension_one': dimension_one,
        'total': total,
        'total_raw': total_raw
    }
  }

  # High-Level Narrative
  for dimension in dimensions:

    output = get_trend_outliers(
      df = df,
      dimension=dimension,
      measure=measure,
      # we need overall total for average only, in other cases it leads to incorrect output
      total = None if summarization in ["sum", "count"] else total_raw,
      summarization = summarization,
      coverage = coverage,
      coverage_limit = coverage_limit
    )

    if output is None:
        continue

    # Outputting all to the global env
    n_outliers = output['n_outliers']
    outlier_levels = output['outlier_levels']
    outlier_values = output['outlier_values']
    outlier_values_p = output['outlier_values_p']

    if summarization == 'average':
      outlier_insight = ', '.join([f"{outlier_levels} ({outlier_values}, {outlier_values_p} vs average {measure})" for outlier_levels, outlier_values, outlier_values_p in zip(outlier_levels, outlier_values, outlier_values_p)])
    else:
      outlier_insight = ', '.join([f"{outlier_levels} ({outlier_values}, {outlier_values_p})" for outlier_levels, outlier_values, outlier_values_p in zip(outlier_levels, outlier_values, outlier_values_p)])

    if n_outliers > 1:
      template_outlier_final = template_outlier_multiple
      template_selected = "multiple"
    else:
      template_outlier_final = template_outlier
      template_selected = "single"

    narrative_outlier_final = {
       f'{dimension} by {measure}': eval(f"f'{template_outlier_final}'")
       }
    
    narrative.update(narrative_outlier_final)

    if template_selected == 'single':
      variables_l1 = { 
         f'{dimension} by {measure}': {
          'narrative_outlier_final': narrative_outlier_final,        
          'template_outlier': template_outlier,        
          'dimension': dimension,        
          'measure': measure,        
          'outlier_insight': outlier_insight,        
          'n_outliers': n_outliers,        
          'outlier_levels': outlier_levels,        
          'outlier_values': outlier_values,        
          'outlier_values_p': outlier_values_p    
          }
        }

    if template_selected == 'multiple':
      variables_l1 = { 
         f'{dimension} by {measure}': {
          'narrative_outlier_final': narrative_outlier_final,        
          'template_outlier_multiple': template_outlier_multiple,        
          'dimension': dimension,        
          'measure': measure,        
          'outlier_insight': outlier_insight,        
          'n_outliers': n_outliers,        
          'outlier_levels': outlier_levels,        
          'outlier_values': outlier_values,        
          'outlier_values_p': outlier_values_p    
          }
        }

    variables.update(variables_l1)
    
  # Output
  if return_data == True:
    return(variables)
   
  if simplify == True:
    narrative = list(narrative.values())
    
  return(narrative)