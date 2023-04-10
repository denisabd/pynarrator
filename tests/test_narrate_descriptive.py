import pandas as pd
from pynarrator import narrate_descriptive
import pytest

def test_narrate_descriptive_returns_dict():
    # Prepare test data
    data = {
        'Region': ['North', 'North', 'South', 'West', 'East', 'East'],
        'Product': ['A', 'B', 'A', 'C', 'C', 'B'],
        'Sales': [10, 15, 20, 5, 25, 30]
    }
    df = pd.DataFrame(data)

    # Test the function
    narrative = narrate_descriptive(df, measure='Sales', dimensions=['Region', 'Product'], coverage=0.4)

    # Assertions
    assert isinstance(narrative, dict)
    assert 'Outlying Product by Sales is B (45, 43.0%).' in narrative.values()
    assert 'Outlying Region by Sales is East (55, 52.0%).' in narrative.values()

def test_narrate_descriptive_simplify_returns_list():
    # Prepare test data
    data = {
        'Region': ['North', 'North', 'South', 'West', 'East', 'East'],
        'Product': ['A', 'B', 'A', 'C', 'C', 'B'],
        'Sales': [10, 15, 20, 5, 25, 30]
    }
    df = pd.DataFrame(data)

    # Test the function
    narrative = narrate_descriptive(df, measure='Sales', dimensions=['Region', 'Product'], coverage=0.4, simplify=True)

    # Assertions
    assert isinstance(narrative, list)


def test_narrate_descriptive_runs():
    # Prepare test data
    data = {
        'Region': ['North', 'North', 'South', 'West', 'East', 'East'],
        'Product': ['A', 'B', 'A', 'C', 'C', 'B'],
        'Sales': [10, 15, 20, 5, 25, 30]
    }
    df = pd.DataFrame(data)

    with pytest.raises(Exception):
        narrate_descriptive(df, measure='Region', dimensions=['Region', 'Sales'])