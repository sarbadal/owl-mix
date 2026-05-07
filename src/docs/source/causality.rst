.. _causality:

Causality Analysis
==================

Causality analysis utilities for time series data.

This module provides the ``CausalityTest`` class, which implements Granger causality testing
between a target variable and other features in a pandas DataFrame. It includes methods for
data validation, low-variance checks, safe execution of statistical tests, and scoring of
causal relationships based on p-values and prediction error (MAPE).

Dependencies
------------

- pandas
- numpy
- statsmodels
- scikit-learn

Typical usage example::

    from owlmix.eda.causality import CausalityTest
    test = CausalityTest(df, target_column="y")
    results = test.run(max_lag=5)

Module Constants
----------------

.. data:: ERROR_THRESHOLD

   Default threshold for Mean Absolute Percentage Error (MAPE) to consider a causal relationship (float, default: 0.15).

Classes
-------

GrangerResult
~~~~~~~~~~~~~

.. class:: GrangerResult

   TypedDict describing the structure of Granger causality test results.

   **Fields:**

   - variable (str): Feature column name.
   - best_lag (int | str): Best lag with minimum p-value.
   - p_value (float | str): p-value for the best lag.
   - min_p_value (float | str): Minimum p-value across lags.
   - score (float | str): Combined score from p-value and MAPE.
   - mape_score (float | str): MAPE score (as percentage).
   - number_of_lags_tested (int | str): Number of lags tested.
   - causal (bool | str): Whether the feature is considered causal.
   - coefficient_sign (str): "positive" or "negative" sign of the coefficient.

CausalityTest
~~~~~~~~~~~~~

.. class:: CausalityTest(df: pandas.DataFrame, target_column: str, columns: list[str] = None)

   Class for performing Granger causality tests on time series data.

   :param df: Input dataframe.
   :type df: pandas.DataFrame
   :param target_column: The target variable for causality testing.
   :type target_column: str
   :param columns: List of feature columns to test. If None, all columns except target are used.
   :type columns: list[str], optional

   **Attributes:**

   - df (pandas.DataFrame): The input dataframe.
   - target_column (str): The target variable.
   - columns (list[str]): List of feature columns to test.

   **Methods:**

   .. method:: run(max_lag=5, error_threshold=ERROR_THRESHOLD, p_value_weight=None, mape_weight=None) -> dict

      Run Granger causality tests for all selected columns.

      :param max_lag: Maximum lag to test (default: 5).
      :type max_lag: int
      :param error_threshold: MAPE threshold for causality (default: ERROR_THRESHOLD).
      :type error_threshold: float
      :param p_value_weight: Weight for the p-value in the score computation.
      :type p_value_weight: float, optional
      :param mape_weight: Weight for the MAPE in the score computation.
      :type mape_weight: float, optional
      :return: Dictionary containing test results and error threshold.
      :rtype: dict

   .. method:: granger_causality(column, max_lag=5, error_threshold=ERROR_THRESHOLD, p_value_weight=None, mape_weight=None) -> GrangerResult

      Perform Granger causality test on the dataset for a given feature.

      :param column: Feature column name.
      :type column: str
      :param max_lag: Maximum lag to test.
      :type max_lag: int
      :param error_threshold: MAPE threshold for causality.
      :type error_threshold: float
      :param p_value_weight: Weight for the p-value in the score computation.
      :type p_value_weight: float, optional
      :param mape_weight: Weight for the MAPE in the score computation.
      :type mape_weight: float, optional
      :return: Result dictionary for the feature.
      :rtype: GrangerResult

   .. method:: calculate_mape(column) -> float

      Calculate Mean Absolute Percentage Error (MAPE) for a feature.

      :param column: Feature column name.
      :type column: str
      :return: MAPE score.
      :rtype: float

   .. method:: _drop_na()

      Drop rows with missing values from the dataframe.

   .. method:: _row_count_check() -> bool

      Check if the dataframe has enough rows for causality testing.

      :return: True if row count >= 10, else False.
      :rtype: bool

   .. method:: _is_low_variance(df, threshold=1e-8) -> bool

      Check if any column has near-zero variance.

      :param df: Dataframe to check.
      :type df: pandas.DataFrame
      :param threshold: Variance threshold.
      :type threshold: float
      :return: True if any column variance is below threshold.
      :rtype: bool

   .. method:: _safe_granger_test(data, max_lag) -> Tuple[Optional[GrangerRawResult], Optional[str]]

      Run Granger test with numerical safety.

      :param data: Input data array.
      :type data: numpy.ndarray
      :param max_lag: Maximum lag to test.
      :type max_lag: int
      :return: Results and error message if any.
      :rtype: Tuple[Optional[GrangerRawResult], Optional[str]]

   .. method:: _extract_granger_stats(results) -> Tuple[List[float], List[numpy.ndarray]]

      Extract p-values and coefficients from Granger test results.

      :param results: Raw results from grangercausalitytests.
      :type results: GrangerRawResult
      :return: List of p-values and coefficients.
      :rtype: Tuple[List[float], List[numpy.ndarray]]

   .. method:: _compute_score(min_p_value, mape_score, p_value_weight=None, mape_weight=None) -> float

      Compute combined score from p-value and MAPE.

      :param min_p_value: Minimum p-value.
      :type min_p_value: float
      :param mape_score: MAPE score.
      :type mape_score: float
      :param p_value_weight: Weight for p-value.
      :type p_value_weight: float, optional
      :param mape_weight: Weight for MAPE.
      :type mape_weight: float, optional
      :return: Combined score.
      :rtype: float

   .. method:: _get_coefficient_sign(coefficients, best_lag) -> str

      Determine coefficient direction for the best lag.

      :param coefficients: List of coefficient arrays.
      :type coefficients: List[numpy.ndarray]
      :param best_lag: Best lag index.
      :type best_lag: int
      :return: "positive" or "negative".
      :rtype: str

   .. method:: _empty_result(column) -> GrangerResult

      Return a standardized empty result.

      :param column: Feature column name.
      :type column: str
      :return: Empty result dictionary.
      :rtype: GrangerResult

See Also
--------

- :mod:`statsmodels.tsa.stattools.grangercausalitytests`
- :class:`sklearn.linear_model.LinearRegression`
- :func:`sklearn.metrics.mean_absolute_percentage_error`