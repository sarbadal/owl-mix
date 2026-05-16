.. _api.analysis.acf-pacf:

➡️ analysis.acf_pacf
====================

.. currentmodule:: owlmix.analysis.acf_pacf

Autocorrelation and partial autocorrelation are essential tools in time series analysis, helping to identify patterns, 
seasonality, and the appropriate lag structure for modeling.

The :class:`AcfPacfAnalyzer` class provides an easy interface to compute the Autocorrelation Function (ACF) 
and Partial Autocorrelation Function (PACF) for specified columns in a pandas DataFrame. 
It leverages the :mod:`statsmodels` library for time series analysis and supports configurable lag and precision settings.

It is particularly useful in identifying lag relationships and temporal dependencies in MMM (Market Mix Modeling) datasets.

Overview
--------

The module exposes a calculator class that:
 
- Accepts a pandas DataFrame
- Computes ACF and PACF values for selected columns
- Supports configurable lag values
- Returns structured output for downstream analysis or visualization


Class Reference
---------------

.. py:class:: AcfPacfParams(columns=None, n_lags=10, precision=4)

  Dataclass for specifying ACF/PACF analysis parameters.

  :param columns: List of column names to include in the analysis. If None, all numeric columns are used.
  :type columns: ``Optional[list[str]]``
  :param n_lags: Number of lag values to compute for ACF and PACF. Default is 10.
  :type n_lags: ``int``
  :param precision: Number of decimal places to round ACF and PACF values. Default is 4.
  :type precision: ``int``

.. py:class:: AcfPacfAnalyzer(df, params)

  Calculates the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF)
  for specified columns in a pandas DataFrame.

  :param df: Input DataFrame containing time series data.
  :type df: ``pandas.DataFrame``
  :param params: Configuration parameters for ACF/PACF analysis.
  :type params: ``AcfPacfParams``

  .. py:method:: generate()

    Calculates ACF and PACF for each specified column.

    :returns: A dictionary with a "data" key containing a list of results for each column.
    :rtype: dict[str, list[dict]]

    Each result dictionary contains:
      - ``column``: Name of the column analyzed.
      - ``n_obs``: Number of non-null observations.
      - ``lags``: List of lag indices.
      - ``acf``: List of ACF values (rounded to specified precision).
      - ``pacf``: List of PACF values (rounded to specified precision).

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

Usage Example
-------------
 
Below is a simple example of how to use the calculator:
 
.. code-block:: python
 
  import pandas as pd
  from owlmix.utils.sample_data_generator import create_sample_data
  from owlmix.analysis.acf_pacf import AcfPacfAnalyzer, AcfPacfParams

    # Sample data
    num_rows = 100 
    df = create_sample_data(n=100)
    params = AcfPacfParams(
        columns=["sales", "radio_spend", "digital_spend"],
        n_lags=5,
        precision=4
    )
    analyzer = AcfPacfAnalyzer(df, params)
    result = analyzer.compute()

    analyzer.print_results_json(result)
    analyzer.print_results(result)

**Result Example**

Result Output - analyzer.print_results_json(result)

.. code-block:: javascript

  [
    {
      "column": "digital_spend",
      "n_obs": 100,
      "lags": [
        0,
        1,
        2,
        3,
        4,
        5
      ],
      "acf": [
        1.0,
        0.079,
        0.0208,
        0.1941,
        -0.1845,
        0.0838
      ],
      "pacf": [
        1.0,
        0.0798,
        0.0149,
        0.1986,
        -0.2338,
        0.1396
      ]
    },
    {
      "column": "radio_spend",
      "n_obs": 94,
      "lags": [
        0,
        1,
        2,
        3,
        4,
        5
      ],
      "acf": [
        1.0,
        -0.0166,
        -0.0108,
        0.1119,
        -0.0763,
        0.0992
      ],
      "pacf": [
        1.0,
        -0.0167,
        -0.0113,
        0.1153,
        -0.0771,
        0.1075
      ]
    },
    {
      "column": "sales",
      "n_obs": 100,
      "lags": [
        0,
        1,
        2,
        3,
        4,
        5
      ],
      "acf": [
        1.0,
        -0.0274,
        0.0339,
        -0.1039,
        0.0685,
        0.0103
      ],
      "pacf": [
        1.0,
        -0.0277,
        0.0338,
        -0.1054,
        0.0657,
        0.0209
      ]
    }
  ]

Result Output - analyzer.print_results(result, include_outliers=False)

.. code-block:: text

  Column: digital_spend (n_obs=100)
    Lag      ACF     PACF
  -----  -------  -------
      0   1.0000   1.0000
      1   0.0790   0.0798
      2   0.0208   0.0149
      3   0.1941   0.1986
      4  -0.1845  -0.2338
      5   0.0838   0.1396

  Column: radio_spend (n_obs=94)
    Lag      ACF     PACF
  -----  -------  -------
      0   1.0000   1.0000
      1  -0.0166  -0.0167
      2  -0.0108  -0.0113
      3   0.1119   0.1153
      4  -0.0763  -0.0771
      5   0.0992   0.1075

  Column: sales (n_obs=100)
    Lag      ACF     PACF
  -----  -------  -------
      0   1.0000   1.0000
      1  -0.0274  -0.0277
      2   0.0339   0.0338
      3  -0.1039  -0.1054
      4   0.0685   0.0657
      5   0.0103   0.0209

Notes
-----

- Only numeric columns are processed; non-numeric columns are skipped.
- Missing values are automatically dropped before computation.
- The class inherits from ``ColumnMixin`` for flexible column selection.

Dependencies
------------

- pandas
- numpy
- statsmodels

See Also
--------

- `statsmodels documentation <https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.acf.html>`_
- `Partial Autocorrelation <https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html>`_

:ref:`Back to Home <home>`