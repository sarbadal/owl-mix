.. _box_plot:

analysis.box_plot
=================

.. currentmodule:: owlmix.analysis.box_plot

Box plot analysis is a robust method for visualizing the distribution and identifying 
outliers in numerical data. This module provides tools to compute box plot statistics 
for selected columns in a pandas DataFrame, supporting both IQR and Z-score methods 
for outlier detection.

The :class:`BoxPlotAnalyzer` class offers a flexible interface for generating box plot 
statistics, with configurable methods, thresholds, and precision.

Overview
--------

The module exposes:

- A parameter dataclass for flexible configuration
- An analyzer class that:

  - Accepts a pandas ``DataFrame``
  - Computes box plot statistics (``min``, ``Q1``, ``median``, ``Q3``, ``max``, ``outliers``) for selected features
  - Supports both IQR and Z-score outlier detection methods
  - Allows configurable precision and outlier thresholds
  - Returns structured output for downstream analysis or visualization

----

Class Reference
---------------

.. py:class:: BoxPlotParams(columns=None, method='iqr', threshold=None, precision=2)

   Dataclass for specifying box plot analysis parameters.

   :param columns: List of column names to include in the analysis. If None, all numeric columns are used.
   :type columns: ``Optional[List[str]]``
   :param method: Method to identify outliers. Options are ``'iqr'`` (Interquartile Range) and ``'zscore'`` (Z-score method). Default is ``'iqr'``.
   :type method: ``str``
   :param threshold: Threshold for identifying outliers. For ``'iqr'``, it's the multiplier for the IQR (default 1.5). For ``'zscore'``, it's the Z-score threshold (default 3.0).
   :type threshold: ``Optional[float]``
   :param precision: Number of decimal places to round statistics. Default is 2.
   :type precision: ``int``

   :raises ValueError: If an unsupported method is provided or precision is negative.

----

.. py:class:: BoxPlotAnalyzer(df, params)

   Analyzer for creating box plot data from a DataFrame.

   :param df: Input DataFrame containing the data.
   :type df: ``pandas.DataFrame``
   :param params: Configuration parameters for box plot analysis.
   :type params: ``BoxPlotParams``

   .. py:method:: compute()

      Computes box plot statistics for each selected column.

      :returns: 
      
        A list of dictionaries, each containing:
            - ``column``: Column name
            - ``min``: Minimum value
            - ``Q1``: First quartile (25th percentile)
            - ``median``: Median (50th percentile)
            - ``Q3``: Third quartile (75th percentile)
            - ``max``: Maximum value
            - ``outliers_count``: Number of detected outliers
            - ``outliers``: List of outlier values
      :rtype: ``list[dict]``

   .. py:method:: print_results_json(results=None, indent=2)

      Prints the results in JSON format.

      :param results: The results to print. If None, uses the computed results.
      :type results: ``list[dict], optional``
      :param indent: Indentation level for pretty-printing the JSON.
      :type indent: ``int``

   .. py:method:: print_results(results=None, include_outliers=False)

      Prints the results in a human-readable tabular format.

      :param results: The results to print. If None, uses the computed results.
      :type results: ``list[dict], optional``
      :param include_outliers: Whether to include the list of outlier values in the table. Default is ``False``.
      :type include_outliers: ``bool``

----

Usage Example
-------------

Below is a simple example of how to use the analyzer:

.. code-block:: python

    import pandas as pd
    from owlmix.utils.sample_data_generator import create_sample_data
    from owlmix.analysis.box_plot import BoxPlotAnalyzer, BoxPlotParams

    df = create_sample_data(n=100)
    params = BoxPlotParams(
        method="zscore",  # or "iqr"
        precision=2
    )
    analyzer = BoxPlotAnalyzer(df, params)
    result = analyzer.compute()
    analyzer.print_results_json(result)
    analyzer.print_results(result, include_outliers=False)

**Result Example**

Result Output - analyzer.print_results_json(result)

.. code-block:: javascript

    [
        {
            "column": "tv_spend",
            "min": 102,
            "Q1": 228,
            "median": 299,
            "Q3": 408,
            "max": 498,
            "outliers_count": 0,
            "outliers": []
        },
        {
            "column": "digital_spend",
            "min": 50,
            "Q1": 115.75,
            "median": 166,
            "Q3": 242.25,
            "max": 294,
            "outliers_count": 0,
            "outliers": []
        },
        ...
    ]

Result Output - analyzer.print_results(result, include_outliers=False)

.. code-block:: text

    Column            Min      Q1    Median      Q3    Max    Outliers Count
    -------------  ------  ------  --------  ------  -----  ----------------
    tv_spend          102     228       299     408    498                 0
    digital_spend      50  115.75       166  242.25    294                 0
    radio_spend        20      53        83  108.75    149                 0
    tv_grp             10   28.75      45.5      79     96                 0
    radio_grp          21    53.5      91.5  120.25    149                 0
    digital_imp        11   31.75      54.5   75.25     98                 0
    radio_imp          20      54      92.5  119.25    149                 0
    inflation          10      32        50   72.25     97                 0
    sales          124.34  194.83       235   281.7  364.8                 0

----

Notes
-----

- Only numeric columns are processed; non-numeric columns are ignored.
- Outlier detection can be performed using either the IQR or Z-score method.
- If no columns are specified, all numeric columns in the DataFrame are analyzed.
- The threshold parameter controls the sensitivity of outlier detection.
- Results can be printed in both JSON and tabular formats.

Dependencies
------------

- pandas
- numpy
- tabulate

See Also
--------

- `Box plot (Wikipedia) <https://en.wikipedia.org/wiki/Box_plot>`_
- `pandas.DataFrame.quantile <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.quantile.html>`_