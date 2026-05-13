.. _correlation:

Correlation Module - Analysis
=============================

.. currentmodule:: owlmix.analysis.correlation

Correlation analysis is a fundamental tool in data analysis, used to measure the strength and direction of relationships between variables. This module provides functionality to compute both the correlation matrix and lagged correlations for selected columns in a pandas DataFrame.

The ``CorrelationAnalyzer`` class offers a convenient interface for correlation analysis, supporting configurable lag values and precision, and is suitable for time series and general data exploration.

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

Class Reference
---------------

.. autoclass:: owlmix.analysis.correlation.CorrelationParams
   :members:
   :show-inheritance:

   Dataclass for specifying correlation analysis parameters.

   :param columns: List of column names to include in the analysis. If None, all numeric columns are used.
   :type columns: Optional[List[str]]
   :param n_lags: Number of lag values to compute for lagged correlation.
   :type n_lags: int
   :param precision: Number of decimal places to round correlation values.
   :type precision: int

.. autoclass:: owlmix.analysis.correlation.CorrelationAnalyzer(df, params)
   :members:
   :show-inheritance:

   Computes the correlation matrix and lagged correlations for specified features in a pandas DataFrame.

   :param df: Input DataFrame containing the data.
   :type df: pandas.DataFrame
   :param params: Configuration parameters for correlation analysis.
   :type params: CorrelationParams

**Example:**

.. code-block:: python

    import pandas as pd
    from owlmix.analysis.correlation import CorrelationAnalyzer, CorrelationParams

    # Example DataFrame
    df = pd.DataFrame({
        "a": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "b": [2, 3, 2, 5, 7, 8, 6, 5, 4, 3],
        "c": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    })

    params = CorrelationParams(
        columns=["a", "b", "c"],
        n_lags=3,
        precision=2
    )

    analyzer = CorrelationAnalyzer(df=df, params=params)
    result = analyzer.compute()
    print(result)

Methods
-------

.. py:method:: compute()

   Computes both the correlation matrix and lagged correlations.

   :returns: A dictionary with keys:
     - ``correlation_matrix``: Nested dictionary representing the correlation matrix.
     - ``lagged_correlation_matrix``: Dictionary mapping each column to its lagged correlations.
   :rtype: dict[str, dict]

.. py:method:: compute_correlation_matrix()

   Computes the correlation matrix for the selected columns.

   :returns: Nested dictionary representing the correlation matrix.
   :rtype: dict[str, dict[str, float]]

.. py:method:: compute_lag_correlation()

   Computes the correlation between a lagged version of a column and the original column for specified lags.

   :returns: Dictionary mapping each column to its lagged correlations.
   :rtype: dict[str, dict[int, float]]

.. py:method:: print_results_json(results=None, indent=2)

   Prints the results in JSON format.

   :param results: The results to print. If None, uses the computed results.
   :type results: dict, optional
   :param indent: Indentation level for pretty-printing the JSON.
   :type indent: int

.. py:method:: print_results(results=None)

   Prints the results in a human-readable tabular format.

   :param results: The results to print. If None, uses the computed results.
   :type results: dict, optional

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
    analyzer.print_results(result)

**Result Example**

.. code-block:: json

    {
        "correlation_matrix": {
            "a": {"a": 1.0, "b": 0.12, "c": 0.98},
            "b": {"a": 0.12, "b": 1.0, "c": 0.15},
            "c": {"a": 0.98, "b": 0.15, "c": 1.0}
        },
        "lagged_correlation_matrix": {
            "a": {"0": 1.0, "1": 0.85, "2": 0.70},
            "b": {"0": 1.0, "1": 0.60, "2": 0.45},
            "c": {"0": 1.0, "1": 0.90, "2": 0.80}
        }
    }

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

See Also
--------

- `pandas.DataFrame.corr <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.corr.html>`_
- `Correlation and dependence (Wikipedia) <https://en.wikipedia.org/wiki/Correlation_and_dependence>`_