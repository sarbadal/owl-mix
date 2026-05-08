.. _acfpacf:

Auto Correlation and Partial Auto Correlation
=============================================

.. currentmodule:: owlmix.eda.acf_pacf

The ``ACFPACFCalculator`` class provides an easy interface to compute the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF) for specified columns in a pandas DataFrame. It leverages the `statsmodels` library for time series analysis and supports configurable lag and precision settings.

Overview
--------

Autocorrelation and partial autocorrelation are essential tools in time series analysis, helping to identify patterns, seasonality, and the appropriate lag structure for modeling.

The ``ACFPACFCalculator`` is designed to:
- Compute ACF and PACF for one or more columns in a DataFrame.
- Allow users to specify the number of lags and decimal precision.
- Return results in a structured dictionary format for further analysis or visualization.

Class Reference
---------------

.. autoclass:: owlmix.eda.acf_pacf.ACFPACFCalculator(df, columns, n_lags=15, precision=3)
   :members:
   :undoc-members:
   :show-inheritance:

   Calculates the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF)
   for specified columns in a pandas DataFrame.

   :param df: Input DataFrame containing time series data.
   :type df: pandas.DataFrame
   :param columns: List of column names to compute ACF/PACF for.
   :type columns: list[str]
   :param n_lags: Number of lags to compute (default: 15).
   :type n_lags: int, optional
   :param precision: Decimal precision for results (default: 3).
   :type precision: int, optional

   **Example:**

   .. code-block:: python

      import pandas as pd
      from owlmix.eda.acf_pacf import ACFPACFCalculator

      # Example DataFrame
      df = pd.DataFrame({
          "col1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
          "col2": [2, 3, 2, 5, 7, 8, 6, 5, 4, 3]
      })

      calculator = ACFPACFCalculator(df, columns=["col1", "col2"], n_lags=5, precision=2)
      result = calculator.generate()
      print(result)

Methods
-------

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

   **Example Output:**

   .. code-block:: python

      {
          "data": [
              {
                  "column": "col1",
                  "n_obs": 10,
                  "lags": [0, 1, 2, 3, 4, 5],
                  "acf": [1.0, 0.8, 0.6, 0.4, 0.2, 0.0],
                  "pacf": [1.0, 0.8, 0.1, -0.2, 0.05, -0.1]
              },
              ...
          ]
      }

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