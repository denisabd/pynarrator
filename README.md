# pynarrator
 Template-based NLG framework for creating text narratives out of data

 ## Installation

 You can install the package from pip:

 ```bash
 pip3 install pynarrator
 ```

 ```python
 import os
 from pynarrator import narrate_descriptive, read_data
```

## Basic Usage

pynarrator has a range of functions for creating template-based narratives and also embedded data set that you can use by calling `read_data()`

```python
sales = read_data()
narrative = narrate_descriptive(sales, measure = 'Sales', dimensions = ['Region', 'Product'], coverage = 0.5)
```

## Chat GPT

```python
 from pynarrator import gpt_get_completions, enhance_narrative, translate_narrative, summarize_narrative
```

```python
enhance_narrative(narrative)
```

```python
enhance_narrative(narrative, language = 'Spanish')
```

```python
summarize_narrative(narrative)
```

Complete documentation is available at the [narrator](https://denisabd.github.io/narrator/) package website
