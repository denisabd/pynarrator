# df = pd.read_csv('sales.csv', keep_default_na=False)
# 
# df.head()
# df.dtypes
# 
# df.select_dtypes(include='number')
# 
# template_total = 'Total {measure} across all {pluralize(dimension_one)} is {total}.'
# eval(f"f'{template_total}'")
import pandas as pd
from pynarrator.pluralize import pluralize

def narrate_descriptive(
  df,
  measure = None,
  dimensions = None,
  summarization = 'sum',
  coverage = 0.5,
  coverage_limit = 5,
  narration_depth = 2,
  template_total = 'Total {measure} across all {pluralize(dimension_one)} is {total}.',
  template_average = 'Average {measure} across all {pluralize(dimension_one)} is {total}.',
  template_outlier = 'Outlying {dimension} by {measure} is {outlier_insight}.',
  template_outlier_multiple = 'Outlying {pluralize(dimension)} by {measure} are {outlier_insight}.',
  template_outlier_l2 = 'In {level_l1}, significant {level_l2} by {measure} is {outlier_insight}.',
  template_outlier_l2_multiple = 'In {level_l1}, significant {pluralize(level_l2)} by {measure} are {outlier_insight}.',
  return_data = False,
  simplify = False
  ):
    
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
    total_raw = df[measure].sum()
  elif summarization == 'average':
    total_raw = df[measure].mean()
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
  
  
  # Output
  if return_data == True:
    return(variables)
   
  if simplify == True:
    narrative = list(narrative.values())
    
  return(narrative)
# 
# df2 = df.groupby(['Region', 'Product']).agg({'Sales': 'sum'}).reset_index()
# df2.shape
# type(df2)
# sum(df2['Sales'])
# narrate_descriptive(df2)
# 
# df3 = df.groupby(['Region', 'Product']).agg({'Sales': 'sum'})
# df3['Sales'].sum().sum()
# 
# narrate_descriptive(df, measure = 'Sales', dimensions = ['Region', 'Product'], return_data=False,  simplify=True)
# 
# measure = 'Sales'
# dimensions = ['Region', 'Product']
# return_data=False
# simplify=True

