.. _api.analysis.correlation:

🔬 analysis.correlation
=======================

.. currentmodule:: owlmix.analysis.correlation

Correlation analysis is a fundamental tool in data analysis, used to measure the strength 
and direction of relationships between variables. This module provides functionality to 
compute both the correlation matrix and lagged correlations for selected columns in a pandas DataFrame.

The :class:`CorrelationAnalyzer` class offers a convenient interface for correlation analysis, 
supporting configurable lag values and precision, and is suitable for time series and general data exploration.

Overview
--------

The module exposes:

- A parameter dataclass for flexible configuration
- An analyzer class that:

  - Accepts a pandas DataFrame
  - Computes the correlation matrix for selected features
  - Computes lagged correlations for each feature up to a specified lag
  - Supports configurable precision
  - Returns structured output for downstream analysis or visualization

----

Class Reference
---------------

.. py:class:: CorrelationParams(columns=None, n_lags=10, precision=4)

    Dataclass for specifying correlation analysis parameters.

    :param columns: List of column names to include in the analysis. If None, all numeric columns are used.
    :type columns: ``Optional[List[str]]``
    :param n_lags: Number of lag values to compute for lagged correlation.
    :type n_lags: ``int``
    :param precision: Number of decimal places to round correlation values.
    :type precision: ``int``

.. py:class:: CorrelationAnalyzer(df, params)

    Computes the correlation matrix and lagged correlations for specified features in a pandas DataFrame.

    :param df: Input DataFrame containing the data.
    :type df: ``pandas.DataFrame``
    :param params: Configuration parameters for correlation analysis.
    :type params: ``CorrelationParams``

    .. py:method:: compute()

        Computes both the correlation matrix and lagged correlations.

        :returns: A dictionary with keys:
          - ``correlation_matrix``: Nested dictionary representing the correlation matrix.
          - ``lagged_correlation_matrix``: Dictionary mapping each column to its lagged correlations.
        :rtype: ``dict[str, dict]``

    .. py:method:: compute_correlation_matrix()

        Computes the correlation matrix for the selected columns.

        :returns: Nested dictionary representing the correlation matrix.
        :rtype: ``dict[str, dict[str, float]]``

    .. py:method:: compute_lag_correlation()

        Computes the correlation between a lagged version of a column and the original column for specified lags.

        :returns: Dictionary mapping each column to its lagged correlations.
        :rtype: ``dict[str, dict[int, float]]``

    .. py:method:: print_results_json(results=None, indent=2)

        Prints the results in JSON format.

        :param results: The results to print. If None, uses the computed results.
        :type results: ``Optional[dict]``
        :param indent: Indentation level for pretty-printing the JSON.
        :type indent: ``int``

    .. py:method:: print_results(results=None)

        Prints the results in a human-readable tabular format.

        :param results: The results to print. If None, uses the computed results.
        :type results: ``Optional[dict]``

----

Usage Example
-------------

Below is a simple example of how to use the analyzer:

.. code-block:: python

    import pandas as pd
    from owlmix.analysis.correlation import CorrelationAnalyzer, CorrelationParams

    df = pd.DataFrame({
        "a": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "b": [2, 3, 2, 5, 7, 8, 6, 5, 4, 3],
        "c": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    })

    params = CorrelationParams(
        columns=["a", "b", "c"],
        n_lags=2,
        precision=2
    )
    analyzer = CorrelationAnalyzer(df=df, params=params)
    result = analyzer.compute()
    analyzer.print_results_json(result)
    analyzer.print_results(result)

**Result Example**

Result Output - analyzer.print_results_json(result) 

.. code-block:: json

    {
        "correlation_matrix": {
            "a": {
                "a": 1.0,
                "b": 0.31,
                "c": 1.0
            },
            "b": {
                "a": 0.31,
                "b": 1.0,
                "c": 0.31
            },
            "c": {
                "a": 1.0,
                "b": 0.31,
                "c": 1.0
            }
        },
        "lagged_correlation_matrix": {
            "a": {
                "0": 1.0,
                "1": 1.0,
                "2": 1.0
            },
            "b": {
                "0": 1.0,
                "1": 0.66,
                "2": 0.13
            },
            "c": {
                "0": 1.0,
                "1": 1.0,
                "2": 1.0
            }
        }
    }

Result Output - analyzer.print_results(result) 

.. code-block:: text

    Correlation Matrix:
        a     b     c
    --  ----  ----  ----
    a   1.00  0.31  1.00
    b   0.31  1.00  0.31
    c   1.00  0.31  1.00

    Lagged Correlation Matrix:
    Column      Lag 0    Lag 1    Lag 2
    --------  -------  -------  -------
    a            1.00     1.00     1.00
    b            1.00     0.66     0.13
    c            1.00     1.00     1.00

----

Notes
-----

- Only numeric columns are processed; non-numeric columns are ignored.
- Missing values are automatically handled by pandas correlation methods.
- If fewer than two columns are provided, correlation is not defined and NaN is returned.
- Lagged correlation is computed for each column up to the specified number of lags.

Dependencies
------------

- pandas
- numpy
- tabulate

References
----------

- :ref:`ACF and PACF Analysis <api.analysis.acf-pacf>`
- :ref:`Box Plot Analysis <api.analysis.box-plot>`
- :ref:`Causality Analysis <api.analysis.causality>`
- :ref:`Cross-Correlation Function Analysis <api.analysis.ccf>`
- :ref:`Correlation Analysis <api.analysis.correlation>`
- :ref:`Variance Inflation Factor Analysis <api.analysis.vif>`
- :ref:`ACF and PACF Plotting <api.plotter.acf-pacf>`
- :ref:`Box Plotting <api.plotter.box-plot>`
- :ref:`Correlation Heatmap Plotting <api.plotter.correlation>`
- :ref:`Variance Inflation Factor Plotting <api.plotter.vif>`

See Also
--------

- `pandas.DataFrame.corr <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.corr.html>`_
- `Correlation and dependence (Wikipedia) <https://en.wikipedia.org/wiki/Correlation_and_dependence>`_

:ref:`Back to Home <home>`