from setuptools import setup
import os

with open('README.md', 'r') as fh:
   long_description = fh.read()
  
setup(
  name = 'pynarrator',
  version = '0.0.1.7',
  author = 'Denis Abdullin',
  author_email = 'denisabdullincz@gmail.com',
  description = 'Template-based NLG framework for creating text narratives out of data',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  py_modules = [
    'narrate_descriptive', 
    'pluralize', 
    'data',
    'chatgpt'
    ],
  package_dir = {'': 'src'},
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
