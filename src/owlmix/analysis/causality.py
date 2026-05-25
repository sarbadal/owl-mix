import inspect
import io
import json
import pandas as pd
import numpy as np
import warnings
from contextlib import redirect_stdout
from typing import Any, List, Dict, Optional, TypedDict, Unpack, Tuple
from dataclasses import dataclass
from statsmodels.tsa.stattools import grangercausalitytests
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
from tabulate import tabulate

from .base import BaseAnalyzer
from ..utils.mixin import ColumnMixin


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


class WeightParams(TypedDict):
    """
    TypedDict describing the structure of weight parameters for score calculation.
    """
    p_value_weight: float
    mape_weight: float


@dataclass
class CausalityParams:
    """
    Parameters for Causality analysis.

    Attributes:
        target_column : Optional[str]
            Name of the target column for causality analysis. If None, no specific target is used.
        columns : Optional[List[str]]
            List of column names to include in the causality analysis. If None, all numeric columns are used.
        max_lag : int
            Maximum number of lag values to compute for causality analysis.
        precision : int
            Number of decimal places to round causality values.
    """
    target_column: Optional[str] = None
    columns: Optional[List[str]] = None
    max_lag: int = 5
    precision: int = 3
    error_threshold: float = 0.15
    p_value_weight: float = 0.60
    mape_weight: float = 0.40


class CausalityAnalyzer(BaseAnalyzer, ColumnMixin):
    """
    Analyzer for computing causality analysis.

    This class computes the causality between a target column and other columns for specified lags.

    Parameters:
        df : pd.DataFrame
            The input DataFrame containing the data.
        params : CausalityParams
            The parameters for causality analysis.
    Attributes:
        target_column : Optional[str]
            Name of the target column for causality analysis. If None, no specific target is used.
        columns : List[str]
            List of column names to include in the causality analysis. If None, all numeric columns are used.
    """

    def __init__(self, df: pd.DataFrame, params: CausalityParams):
        super().__init__(df, params)
        self.target_column = params.target_column
        self.columns = [
            col
            for col in self._get_numeric_columns(params.columns)
            if col != self.target_column
        ]
        self.max_lag = params.max_lag
        self.precision = params.precision
        self.error_threshold = params.error_threshold
        self.p_value_weight = params.p_value_weight
        self.mape_weight = params.mape_weight

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
        df = self.df[[self.target_column, column]].copy()
        df = df.dropna()

        X = df[[column]]
        y = df[self.target_column]
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        mape = mean_absolute_percentage_error(y, y_pred)
        return mape

    def _is_low_variance(self, df: pd.DataFrame, threshold: float = 1e-8) -> bool:
        """
        Check if any column has near-zero variance.
        Args:
            df (pd.DataFrame): DataFrame to check.
            threshold (float): Variance threshold.
        Returns:
            bool: True if any column variance is below threshold.
        """
        std_series = df.std()
        return bool((std_series < threshold).any())

    def _safe_granger_test(self, data: np.ndarray, safe_lag: int) -> Tuple[Optional[GrangerRawResult], Optional[str]]:
        """
        Run Granger test with numerical safety.
        Args:
            data (np.ndarray): Input data array.
        Returns:
            Tuple[Optional[GrangerRawResult], Optional[str]]: Results and error message if any.
        """
        try:
            func = grangercausalitytests
            try:
                has_verbose = "verbose" in inspect.signature(func).parameters
            except (TypeError, ValueError):
                # Fallback if signature introspection is unavailable
                has_verbose = True
        
            call_kwargs: Dict[str, Any] = {"maxlag": safe_lag}
            if has_verbose:
                call_kwargs["verbose"] = False

            with warnings.catch_warnings():
                warnings.filterwarnings("error", category=RuntimeWarning)
                warnings.filterwarnings(
                    "ignore",
                    message="verbose is deprecated since functions should not print results",
                    category=FutureWarning,
                    module=r"statsmodels\.tsa\.stattools",
                )
                with np.errstate(divide="raise", invalid="raise"):
                    with redirect_stdout(io.StringIO()):
                        results = func(
                            data,
                            **call_kwargs
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
        p_score = (1 - min_p_value) * (self.p_value_weight * 100)
        e_score = (1 - min(mape_score, 1)) * (self.mape_weight * 100)
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
            "best_lag": "n/a",
            "p_value": "n/a",
            "min_p_value": "n/a",
            "score": "n/a",
            "mape_score": "n/a",
            "number_of_lags_tested": "n/a",
            "causal": "n/a",
            "coefficient_sign": "n/a",
        }

    def granger_causality(self, column: str) -> GrangerResult:
        """
        Perform Granger causality test on the dataset for a given feature.

        Args:
            column (str): Feature column name.

        Returns:
            GrangerResult: Result dictionary for the feature.
        """
        self._drop_na()

        if not self._row_count_check():
            print(f"Not enough data to perform Granger causality test for column '{column}'. "
                  f"Minimum 10 rows required.")
            return self._empty_result(column)
        
        df = self.df[[self.target_column, column]].copy()
        df = df.diff().dropna()

        # Low variance check
        if (self._is_low_variance(df)) or (len(df) < self.max_lag + 1):
            return self._empty_result(column)

        # Numeric validation
        if not all(np.issubdtype(dtype, np.number) for dtype in df.dtypes):
            raise ValueError("Selected columns must be numeric.")

        data: np.ndarray = df.values
        safe_lag: int = min(self.max_lag, max(1, len(data) // 5))
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
                (min_p_value < 0.05) and (mape_score < self.error_threshold)
        )

        return {
            "variable": column,
            "best_lag": best_lag,
            "p_value": round(min_p_value, self.precision),
            "min_p_value": min_p_value,
            "score": score,
            "mape_score": round(mape_score * 100, self.precision),
            "number_of_lags_tested": len(p_values),
            "causal": causality,
            "coefficient_sign": coefficient_sign,
        }

    def compute(self) -> List[GrangerResult]:
        """
        Compute Granger causality results for all selected columns.

        Returns:
            List[GrangerResult]: List of result dictionaries for each feature.
        """
        results: List[GrangerResult] = []
        for column in self.columns:
            if column == self.target_column:
                continue
            result = self.granger_causality(column)
            results.append(result)
        return {
            "causality_test_results": results,
            "error_threshold": self.error_threshold * 100
        }

    def print_results_json(self, results: list[dict] = None, indent: int = 2):
        """
        Print the results in JSON format.

        Args:
            results (list[dict], optional): The results to print. If None, uses the computed correlation and lagged correlation.
            indent (int): The indentation level for pretty-printing the JSON.
        """
        if results is None:
            results = self.compute()
        print(json.dumps(results, indent=indent))

    def print_results(self, results: dict = None) -> None:
        """
        Print the results in a human-readable tabular format.

        Args:
            results (dict, optional): The results to print. If None, uses the computed correlation and lagged correlation.
        """        
        if results is None:
            results = self.compute()

        print(f"Granger Causality Test Results (Target: '{self.target_column}')")
        print(f"Combined Score Weights -> P-Value: {self.p_value_weight * 100}%, MAPE: {self.mape_weight * 100}%")
        print(f"Error Threshold for MAPE: {self.error_threshold * 100}%\n")
        table_data = []
        for res in results.get("causality_test_results", []):
            table_data.append([
                res.get("variable"),
                res.get("best_lag"),
                res.get("p_value"),
                res.get("mape_score"),
                res.get("score"),
                res.get("causal"),
                res.get("coefficient_sign")
            ])
        headers = ["Variable", "Best Lag", "P-Value", "MAPE Score", "Score", "Causal", "Coefficient Sign"]
        print(tabulate(table_data, headers=headers, tablefmt="simple", floatfmt=f".{self.precision}f"))