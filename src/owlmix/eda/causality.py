# owlmix/eda/causality.py
"""
Causality analysis utilities for time series data.

This module provides the `CausalityTest` class, which implements Granger causality testing
between a target variable and other features in a pandas DataFrame. It includes methods for
data validation, low-variance checks, safe execution of statistical tests, and scoring of
causal relationships based on p-values and prediction error (MAPE).

Classes:
    GrangerResult: TypedDict describing the structure of Granger causality test results.
    CausalityTest: Main class for running Granger causality tests on time series data.

Dependencies:
    - pandas
    - numpy
    - statsmodels
    - scikit-learn

Typical usage example:
    test = CausalityTest(df, target_column="y")
    results = test.run(max_lag=5)
"""

import warnings
import pandas as pd
import numpy as np

from typing import Dict, Any, List, Tuple, Optional, TypedDict, Literal

from statsmodels.tsa.stattools import grangercausalitytests

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error

from .utils import ColumnMixin

warnings.simplefilter(action='ignore', category=FutureWarning)

ERROR_THRESHOLD = 0.15

class GrangerResult(TypedDict, total=False):
    """
    TypedDict describing the structure of Granger causality test results.
    """
    variable: str
    best_lag: int | str
    p_value: float | str
    min_p_value: float | str
    score: float | str
    mape_score: float | str
    number_of_lags_tested: int | str
    causal: bool | str
    coefficient_sign: str

GrangerRawResult = Dict[int, Dict[str, Any]]

class CausalityTest(ColumnMixin):
    """
    Class for performing Granger causality tests on time series data.

    Attributes:
        df (pd.DataFrame): The input dataframe.
        target_column (str): The target variable for causality testing.
        columns (list[str]): List of feature columns to test against the target.
    """
    def __init__(self, df: pd.DataFrame, target_column: str, columns: list[str] = None):
        """
        Initialize the CausalityTest object.

        Args:
            df (pd.DataFrame): Input dataframe.
            target_column (str): The target variable.
            columns (list[str], optional): List of columns to test. If None, all columns except target are used.
        """
        self.df = df.copy()
        self.target_column = target_column
        self.columns = self._get_columns(columns)

    def _drop_na(self):
        """
        Drop rows with missing values from the dataframe.
        """
        self.df = self.df.dropna()

    def _row_count_check(self):
        """
        Check if the dataframe has enough rows for causality testing.

        Returns:
            bool: True if row count >= 10, else False.
        """
        return len(self.df) >= 10

    def calculate_mape(self, column: str) -> float:
        """
        Calculate Mean Absolute Percentage Error (MAPE) for a feature.

        Args:
            column (str): Feature column name.

        Returns:
            float: MAPE score.
        """
        df = self.df.copy()
        X = df[[column]]
        y = df[self.target_column]

        model = LinearRegression()
        model.fit(X, y)
        prediction = model.predict(X)

        mape_score = mean_absolute_percentage_error(y, prediction)

        return mape_score

    def _is_low_variance(self, df: pd.DataFrame, threshold: float = 1e-8) -> bool:
        """
        Check if any column has near-zero variance.

        Args:
            df (pd.DataFrame): Dataframe to check.
            threshold (float): Variance threshold.

        Returns:
            bool: True if any column variance is below threshold.
        """
        std_series = df.std()
        return bool((std_series < threshold).any())

    def _safe_granger_test(self, data: np.ndarray, max_lag: int) -> Tuple[Optional[GrangerRawResult], Optional[str]]:
        """
        Run Granger test with numerical safety.

        Args:
            data (np.ndarray): Input data array.
            max_lag (int): Maximum lag to test.

        Returns:
            Tuple[Optional[GrangerRawResult], Optional[str]]: Results and error message if any.
        """
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("error", category=RuntimeWarning)
                with np.errstate(divide="raise", invalid="raise"):
                    results = grangercausalitytests(
                        data,
                        maxlag=max_lag,
                        verbose=False
                    )
            return results, None
        except (RuntimeWarning, FloatingPointError) as e:
            return None, str(e)

    def _extract_granger_stats(self, results: GrangerRawResult) -> Tuple[List[float], List[np.ndarray]]:
        """
        Extract p-values and coefficients from Granger test results.

        Args:
            results (GrangerRawResult): Raw results from grangercausalitytests.

        Returns:
            Tuple[List[float], List[np.ndarray]]: List of p-values and coefficients.
        """
        p_values: List[float] = []
        coefficients: List[np.ndarray] = []

        for lag in results:
            test_result = results[lag][0]["ssr_ftest"]
            p_values.append(float(test_result[1]))

            ols_model = results[lag][1][1]
            lag_coefficients = ols_model.params[:-1]
            coefficients.append(lag_coefficients)

        return p_values, coefficients

    def _compute_score(self, min_p_value: float, mape_score: float) -> float:
        """
        Compute combined score from p-value and MAPE.

        Args:
            min_p_value (float): Minimum p-value.
            mape_score (float): MAPE score.

        Returns:
            float: Combined score.
        """
        p_score = (1 - min_p_value) * 60
        e_score = (1 - min(mape_score, 1)) * 40
        return round(p_score + e_score, 2)

    def _get_coefficient_sign(self, coefficients: List[np.ndarray], best_lag: int) -> str:
        """
        Determine coefficient direction for the best lag.

        Args:
            coefficients (List[np.ndarray]): List of coefficient arrays.
            best_lag (int): Best lag index.

        Returns:
            str: "positive" or "negative".
        """
        best_coefficients = coefficients[best_lag - 1]
        avg_coefficient = float(np.mean(best_coefficients[:best_lag]))
        return "positive" if avg_coefficient > 0 else "negative"

    def _empty_result(self, column: str) -> GrangerResult:
        """
        Return a standardized empty result.

        Args:
            column (str): Feature column name.

        Returns:
            GrangerResult: Empty result dictionary.
        """
        return {
            "variable": column,
            "best_lag": None,
            "p_value": None,
            "min_p_value": None,
            "score": None,
            "mape_score": None,
            "number_of_lags_tested": None,
            "causal": None,
            "coefficient_sign": None,
        }

    def granger_causality(self, column: str, max_lag: int = 5, error_threshold: float = ERROR_THRESHOLD) -> GrangerResult:
        """
        Perform Granger causality test on the dataset for a given feature.

        Args:
            column (str): Feature column name.
            max_lag (int): Maximum lag to test.
            error_threshold (float): MAPE threshold for causality.

        Returns:
            GrangerResult: Result dictionary for the feature.
        """
        self._drop_na()

        if not self._row_count_check():
            raise ValueError(
                "Not enough data points for Granger causality test. At least 10 rows are required."
            )

        df = self.df[[self.target_column, column]].copy()

        # Low variance check
        if self._is_low_variance(df):
            return self._empty_result(column)

        # Numeric validation
        if not all(np.issubdtype(dtype, np.number) for dtype in df.dtypes):
            raise ValueError("Selected columns must be numeric.")

        # Stationarity
        df = df.diff().dropna()

        if len(df) < 10:
            raise ValueError("Too few rows after differencing.")

        data: np.ndarray = df.values
        safe_lag: int = min(max_lag, max(1, len(data) // 5))

        if safe_lag < 1:
            raise ValueError("Insufficient data for lag computation.")

        # Safe execution
        results, error = self._safe_granger_test(data, safe_lag)

        if error or results is None:
            return self._empty_result(column)

        # Extract stats
        p_values, coefficients = self._extract_granger_stats(results)

        min_p_value: float = min(p_values)
        best_lag: int = p_values.index(min_p_value) + 1

        # Scoring
        mape_score: float = float(self.calculate_mape(column))
        score: float = self._compute_score(min_p_value, mape_score)

        # Interpretation
        coefficient_sign: str = self._get_coefficient_sign(coefficients, best_lag)

        causality: bool = (
                (min_p_value < 0.05) and (mape_score < error_threshold)
        )

        return {
            "variable": column,
            "best_lag": best_lag,
            "p_value": round(min_p_value, 5),
            "min_p_value": min_p_value,
            "score": score,
            "mape_score": round(mape_score * 100, 2),
            "number_of_lags_tested": len(p_values),
            "causal": causality,
            "coefficient_sign": coefficient_sign,
        }

    def run(self, max_lag: int = 5, error_threshold: float = ERROR_THRESHOLD) -> dict[dict[str, Any]]:
        """
        Run Granger causality tests for all selected columns.

        Args:
            max_lag (int): Maximum lag to test.
            error_threshold (float): MAPE threshold for causality.

        Returns:
            dict: Dictionary containing test results and error threshold.
        """
        if self.columns is None:
            self.columns = [col for col in self.df.columns if col != self.target_column]

        results = []
        for column in self.columns:
            result = self.granger_causality(column, max_lag, error_threshold)
            results.append(result)

        return {
            "causality_test_results": results,
            "error_threshold": error_threshold * 100
        }