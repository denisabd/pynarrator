# pynarrator
Template-based NLG framework for creating text narratives out of data

## Installation

You can install the package from pip:

```python
pip3 install pynarrator
```

## Usage

Import the package functions and create a data frame.

```python
from pynarrator import narrate_descriptive, read_data

df = read_data()

df.head()
```

Now create descriptive narratives from your data
```python
narrate_descriptive(df, measure = 'Sales', dimensions = ['Region', 'Product'])
```
