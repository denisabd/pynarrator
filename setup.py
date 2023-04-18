from setuptools import setup, find_packages
import os

with open('README.md', 'r') as fh:
   long_description = fh.read()
  
setup(
  name = 'pynarrator',
  version = '0.0.1.13',
  author = 'Denis Abdullin',
  author_email = 'denisabdullincz@gmail.com',
  description = 'Template-based NLG framework for creating text narratives out of data',
  long_description_content_type = 'text/markdown',
  long_description = long_description,
  py_modules = [
    'chatgpt',
    'clean_text',
    'data',
    'format_pct',
    'format_text',
    'get_frequency',
    'narrate_descriptive', 
    'narrate_trend',
    'pluralize', 
    'tags',
    'ytd'
    ],
  packages = find_packages(),
  install_requires = ['pandas >= 1.0.0', 'inflect >= 6.0.0', 'openai'],
  extras_require = {'dev': ['pytest >= 3.7']},
  keywords = ['python', 'nlg', 'template', 'chatgpt'],
  classifiers = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Operating System :: OS Independent"
  ],
  include_package_data = True,
  package_data = {'': ['data/*.csv']}
)
