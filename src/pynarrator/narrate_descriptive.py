import pandas as pd

df = pd.read_csv("sales.csv")

df.head()

def narrate_descriptive(df):
  # 
  if not isinstance(df, pd.DataFrame):
    print("df must be a pandas DataFrame")
    return
    
  out = df.head(10)
  return(out)


narrate_descriptive(df)

