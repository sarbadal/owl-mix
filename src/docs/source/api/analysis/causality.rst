.. _causality:

Causality Module - Analysis
===========================

.. currentmodule:: owlmix.analysis.causality

Causality analysis helps determine whether one time series can be used to forecast another, 
using statistical tests such as Granger causality. This module provides tools to analyze causal 
relationships between a target variable and other features in a pandas DataFrame, with 
configurable lags, scoring, and error thresholds.

The ``CausalityAnalyzer`` class offers a convenient interface for causality analysis, 
supporting flexible configuration and structured output for downstream analysis or visualization.

Overview
--------

The module exposes:

- A parameter dataclass for flexible configuration
- An analyzer class that:

  - Accepts a pandas DataFrame
  - Computes Granger causality tests for selected features against a target
  - Supports configurable lag values, precision, and scoring weights
  - Returns structured output for further analysis or reporting

----

Class Reference
---------------

.. toggle:: click to expand

    .. autoclass:: owlmix.analysis.causality.CausalityParams
    :members:
    :show-inheritance:

    Dataclass for specifying causality analysis parameters.

    :param target_column: Name of the target column for causality analysis.
    :type target_column: Optional[str]
    :param columns: List of column names to include in the analysis. If None, all numeric columns except the target are used.
    :type columns: Optional[List[str]]
    :param max_lag: Maximum number of lag values to compute for causality analysis.
    :type max_lag: int
    :param precision: Number of decimal places to round causality values.
    :type precision: int
    :param error_threshold: MAPE error threshold for considering a relationship causal (default 0.15).
    :type error_threshold: float
    :param p_value_weight: Weight for p-value in combined score (default 0.60).
    :type p_value_weight: float
    :param mape_weight: Weight for MAPE in combined score (default 0.40).
    :type mape_weight: float

    .. autoclass:: owlmix.analysis.causality.CausalityAnalyzer(df, params)
    :members:
    :show-inheritance:

    Computes Granger causality between a target column and other features in a pandas DataFrame.

    :param df: Input DataFrame containing the data.
    :type df: pandas.DataFrame
    :param params: Configuration parameters for causality analysis.
    :type params: CausalityParams

----

Methods
-------

.. py:method:: compute()

   Computes Granger causality results for all selected columns.

   :returns: A dictionary with keys:
     - ``causality_test_results``: List of result dictionaries for each feature.
     - ``error_threshold``: The MAPE error threshold used for determining causality.
   :rtype: dict

.. py:method:: granger_causality(column)

   Perform Granger causality test for a given feature column.

   :param column: Feature column name.
   :type column: str
   :returns: Result dictionary for the feature.
   :rtype: dict

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

----

Usage Example
-------------

Below is a simple example of how to use the analyzer:

.. code-block:: python

    import pandas as pd
    from owlmix.analysis.causality import CausalityAnalyzer, CausalityParams

    data = {
        "time": [
            "2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05",
            "2021-01-06", "2021-01-07", "2021-01-08", "2021-01-09", "2021-01-10",
            "2021-01-11", "2021-01-12", "2021-01-13", "2021-01-14", "2021-01-15"
        ],
        "tv_spend": [485, 439, 191, 466, 363, 134, 305, 180, 149, 459, 487, 101, 489, 153, 205],
        "digital_spend": [53, 103, 270, 240, 195, 267, 93, 211, 251, 239, 277, 63, 144, 97, 64],
        "radio_spend": [59, 101, 130, 72, 43, 143, 60, 34, 64, 84, 108, 90, 28, 107, 148],
        "tv_grp": [17, 97, 72, 20, 90, 17, 44, 44, 42, 14, 50, 37, 16, 82, 81],
        "radio_grp": [31, 52, 67, 81, 56, 118, 123, 54, 120, 20, 24, 122, 46, 34, 109],
        "digital_imp": [51, 86, 60, 72, 61, 13, 32, 24, 52, 38, 45, 22, 41, 80, 68],
        "radio_imp": [105, 47, 85, 64, 81, 47, 47, 127, 63, 103, 49, 94, 147, 111, 148],
        "inflation": [36, 71, 86, 12, 79, 81, 36, 18, 71, 46, 60, 53, 33, 88, 68],
        "sales": [
            207.898777, 209.953701, 239.238864, 336.879175, 256.028984,
            198.429908, 168.349363, 170.848276, 227.846954, 279.747814,
            316.816354, 116.078746, 254.455082, 149.819427, 163.205816
        ]
    }

    # Create sample data
    df = pd.DataFrame(data)

    # Define parameters for causality analysis
    params = CausalityParams(
        target_column="sales",
        columns=None,  # Use all numeric columns except target
        max_lag=5,
        precision=2,
        p_value_weight=0.2,
        mape_weight=0.8
    )

    # Initialize and compute causality analysis
    analyzer = CausalityAnalyzer(df, params)
    results = analyzer.compute()

    # Print results in JSON format
    analyzer.print_results_json(results)

    # Print results in tabular format
    analyzer.print_results(results)

**Result Example**

Result Output - analyzer.print_results_json(results)

.. toggle:: click to expand

    .. code-block:: json

        {
            "causality_test_results": [
                {
                "variable": "tv_spend",
                "best_lag": 2,
                "p_value": 0.19,
                "min_p_value": 0.18989159332275993,
                "score": 81.36,
                "mape_score": 18.55,
                "number_of_lags_tested": 2,
                "causal": false,
                "coefficient_sign": "positive"
                },
                {
                "variable": "digital_spend",
                "best_lag": 2,
                "p_value": 0.52,
                "min_p_value": 0.52041784926114,
                "score": 74.26,
                "mape_score": 19.16,
                "number_of_lags_tested": 2,
                "causal": false,
                "coefficient_sign": "negative"
                },
                {
                "variable": "radio_spend",
                "best_lag": 1,
                "p_value": 0.93,
                "min_p_value": 0.9262377701806171,
                "score": 62.22,
                "mape_score": 24.07,
                "number_of_lags_tested": 2,
                "causal": false,
                "coefficient_sign": "negative"
                },
                {
                "variable": "tv_grp",
                "best_lag": 2,
                "p_value": 0.37,
                "min_p_value": 0.3684294069543816,
                "score": 72.53,
                "mape_score": 25.12,
                "number_of_lags_tested": 2,
                "causal": false,
                "coefficient_sign": "negative"
                },
                {
                "variable": "radio_grp",
                "best_lag": 2,
                "p_value": 0.53,
                "min_p_value": 0.5257051078063723,
                "score": 71.94,
                "mape_score": 21.93,
                "number_of_lags_tested": 2,
                "causal": false,
                "coefficient_sign": "negative"
                },
                {
                "variable": "digital_imp",
                "best_lag": 2,
                "p_value": 0.24,
                "min_p_value": 0.23860646839310135,
                "score": 75.89,
                "mape_score": 24.17,
                "number_of_lags_tested": 2,
                "causal": false,
                "coefficient_sign": "negative"
                },
                {
                "variable": "radio_imp",
                "best_lag": 1,
                "p_value": 0.25,
                "min_p_value": 0.25250187960913634,
                "score": 75.42,
                "mape_score": 24.41,
                "number_of_lags_tested": 2,
                "causal": false,
                "coefficient_sign": "negative"
                },
                {
                "variable": "inflation",
                "best_lag": 2,
                "p_value": 0.69,
                "min_p_value": 0.6938008037240203,
                "score": 65.97,
                "mape_score": 25.19,
                "number_of_lags_tested": 2,
                "causal": false,
                "coefficient_sign": "negative"
                }
            ],
            "error_threshold": 15.0
        }

Result Output - analyzer.print_results(results)

.. toggle:: click to expand

    .. code-block:: text

        Granger Causality Test Results (Target: 'sales')
        Combined Score Weights -> P-Value: 20.0%, MAPE: 80.0%
        Error Threshold for MAPE: 15.0%

        Variable         Best Lag    P-Value    MAPE Score    Score  Causal    Coefficient Sign
        -------------  ----------  ---------  ------------  -------  --------  ------------------
        tv_spend                2       0.19         18.55    81.36  False     positive
        digital_spend           2       0.52         19.16    74.26  False     negative
        radio_spend             1       0.93         24.07    62.22  False     negative
        tv_grp                  2       0.37         25.12    72.53  False     negative
        radio_grp               2       0.53         21.93    71.94  False     negative
        digital_imp             2       0.24         24.17    75.89  False     negative
        radio_imp               1       0.25         24.41    75.42  False     negative
        inflation               2       0.69         25.19    65.97  False     negative

----

Notes
-----

- Only numeric columns are processed; non-numeric columns are ignored.
- Missing values are automatically dropped before analysis.
- If fewer than 10 rows are available, causality is not computed for that feature.
- Lagged causality is computed for each feature up to the specified number of lags.
- The combined score is a weighted sum of p-value and MAPE, as configured in the parameters.
- The ``causal`` flag is True if p-value < 0.05 and MAPE < error_threshold.

Dependencies
------------

- pandas
- numpy
- statsmodels
- scikit-learn
- tabulate

See Also
--------

- `Granger causality (Wikipedia) <https://en.wikipedia.org/wiki/Granger_causality>`_
- `statsmodels.tsa.stattools.grangercausalitytests <https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.grangercausalitytests.html>`_