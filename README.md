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

pynarrator has a range of functions for creating template-based narratives and also embedded data set that you can use by calling `read_data()`. Function downloads raw data from github, if you get a SSL error when running it, please run this first:

```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

```python
sales = read_data()
narrative = narrate_descriptive(sales, measure = 'Sales', dimensions = ['Region', 'Product'], coverage = 0.5)
```

{'Total Sales': 'Total Sales across all Regions is 38790478.42.',
 'Region by Sales': 'Outlying Regions by Sales are NA (18079736.4, 47.0%), EMEA (13555412.7, 35.0%).',
 'Product by Sales': 'Outlying Products by Sales are Food & Beverage (15543469.7, 40.0%), Electronics (8608962.8, 22.0%).'}

## Chat GPT

In order to use ChatGPT in pynarrator, you must specify your OpenAI API token as `OPENAI_API_KEY` environment variable:

```python
os.environ['OPENAI_API_KEY'] = 'xx-xxxxxxxxxx'
```

```python
 from pynarrator import gpt_get_completions, enhance_narrative, translate_narrative, summarize_narrative
```

Improve the narrative text to make it rich with business language

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
