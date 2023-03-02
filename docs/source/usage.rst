Usage
=====

.. _installation:

Installation
------------

To use pynarrator, first install it using pip:

.. code-block:: console

   pip3 install pynarrator

Descriptive Narratives
----------------

To retrieve a list of random ingredients,
you can use the ``pynarrator.narrate_descriptive()`` function:

For example:

>>> from pynarrator import narrate_descriptive, read_data
>>> df = read_data()
>>> narrate_descriptive(df, measure = 'Sales', dimensions = ['Region', 'Product'])

