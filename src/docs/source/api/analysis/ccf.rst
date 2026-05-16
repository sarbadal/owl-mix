.. _api.analysis.ccf:

🔬 analysis.ccf
===============

.. currentmodule:: owlmix.analysis.ccf

Cross-Correlation Function (CCF) analysis helps identify the relationship between 
a target time series and one or more feature time series, across a range of lags. 
This module provides tools to compute CCF values, summarize results, and support 
feature engineering or time series modeling.

The :class:`CCFAnalyzer` class offers a flexible interface for CCF analysis, 
supporting multiple feature transformations (original, adstocked, differenced), 
configurable lags, and structured output for downstream analysis or visualization.

Overview
--------

The module exposes:

- A parameter dataclass for flexible configuration
- An analyzer class that:
  
  - Accepts a pandas DataFrame
  - Computes CCF for selected features against a target, across multiple lags
  - Supports feature transformations (original, adstocked, differenced)
  - Returns structured output and summary tables for further analysis or reporting

Class Reference
---------------

.. py:class:: CCFParams(time_column=None, target_column=None, feature_columns=None, max_lag=5)

    Dataclass for specifying CCF analysis parameters.

    :param time_column: Name of the time column in the DataFrame. If None, the index is used.
    :type time_column: ``Optional[str]``
    :param target_column: Name of the target column for CCF analysis. If None, the first numeric column is used.
    :type target_column: ``Optional[str]``
    :param feature_columns: List of feature column names to include. If None, all numeric columns except the target are used.
    :type feature_columns: ``Optional[List[str]]``
    :param max_lag: Maximum lag to compute for CCF (lags from 0 to max_lag).
    :type max_lag: ``int``

.. py:class:: CCFAnalyzer(df, params, transformer=default_transformer)

    Computes Cross-Correlation Function (CCF) between a target column and feature columns in a pandas DataFrame.

    :param df: Input DataFrame containing the data.
    :type df: ``pandas.DataFrame``
    :param params: Configuration parameters for CCF analysis.
    :type params: ``CCFParams``
    :param transformer: Optional adstock transformer for feature engineering.
    :type transformer: ``Optional[AdstockTransformer]``

    .. py:method:: compute()

        Computes CCF results for all selected features and their transformed versions.

        :returns: A dictionary with keys:
            - ``ccf_results``: Dictionary mapping feature_version to list of CCF result dicts.
            - ``summary_table``: List of summary dicts for each feature/version.
        :rtype: ``dict``

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

Usage Example
-------------

Below is a simple example of how to use the analyzer:

.. code-block:: python

    import pandas as pd
    from owlmix.analysis.ccf import CCFAnalyzer, CCFParams

    data = {
        "time": [
            "2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"
        ],
        "feature1": [10, 20, 30, 40, 50],
        "feature2": [5, 3, 6, 2, 7],
        "target": [100, 110, 120, 130, 140]
    }

    df = pd.DataFrame(data)

    params = CCFParams(
        time_column="time",
        target_column="target",
        feature_columns=None,  # Use all numeric columns except target
        max_lag=2
    )

    analyzer = CCFAnalyzer(df, params)
    results = analyzer.compute()

    analyzer.print_results_json(results)
    analyzer.print_results(results)

**Result Example**

Result Output - ``analyzer.print_results_json(results)``

.. code-block:: javascript

    {
        "ccf_results": {
            "feature1_original": [
                {"target_column": "target", "feature": "feature1", "version": "original", "lag": 0, "correlation": 1.0},
                {"target_column": "target", "feature": "feature1", "version": "original", "lag": 1, "correlation": 0.98},
                ...
            ],
            "feature1_adstocked": [
                ...
            ],
            "feature1_differenced": [
                ...
            ],
            ...
        },
        "summary_table": [
            {
                "target_column": "target",
                "feature": "feature1",
                "version": "original",
                "max_correlation": 1.0,
                "lag_at_max": 0,
                "correlation_at_lag_0": 1.0
            },
            ...
        ]
    }

Result Output - ``analyzer.print_results(results)``

.. code-block:: text

    Combined CCF Results for All Features:
    target_column    feature    version     lag     correlation
    --------------  --------   --------   -----  --------------
    target          feature1   original       0           1.000
    target          feature1   original       1           0.980
    ...

    Summary Table:
    target_column    feature    version      max_correlation    lag_at_max    correlation_at_lag_0
    --------------  ---------  ---------  -----------------  ------------  -----------------------
    target           feature1   original                1.0             0                      1.0
    ...

Notes
-----

- Only numeric columns are processed; non-numeric columns are ignored.
- Missing values are automatically dropped before analysis.
- For each feature, CCF is computed for original, adstocked, and differenced versions (if applicable).
- The summary table reports the maximum absolute correlation, the lag at which it occurs, and the correlation at lag 0.
- The adstock transformation is applied if a transformer is provided.

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

- `Cross-correlation (Wikipedia) <https://en.wikipedia.org/wiki/Cross-correlation>`_
- `statsmodels.tsa.stattools.ccf <https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.ccf.html>`_

:ref:`Back to Home <home>`