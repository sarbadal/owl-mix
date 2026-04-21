# src/owlmix/eda/causality.py
import pandas as pd
import numpy as np

from statsmodels.tsa.stattools import grangercausalitytests

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
from typing import Any

import warnings

from .utils import ColumnMixin

warnings.simplefilter(action='ignore', category=FutureWarning)


class CausalityTest(ColumnMixin):
    def __init__(self, df: pd.DataFrame, target_column: str, columns: list[str] = None):
        self.df = df.copy()
        self.target_column = target_column
        self.columns = self._get_columns(columns)

    def _drop_na(self):
        self.df = self.df.dropna()

    def _row_count_check(self):
        if len(self.df) < 10:
            return False

    def granger_causality(self, column: str, max_lag: int = 5, error_threshold: float = 0.30):
        """Perform Granger causality test on the dataset."""
        self._drop_na()
        if self._row_count_check() is False:
            raise ValueError("Not enough data points for Granger causality test. At least 10 rows are required.")

        selected_cols = [self.target_column, column]
        df = self.df[selected_cols].copy()

        if not all(np.issubdtype(dtype, np.number) for dtype in df.dtypes):
            raise ValueError("Selected columns must be numeric.")

        # Differencing (stationarity)
        df = df.diff().dropna()

        if len(df) < 10:
            raise ValueError("Too few rows after differencing.")

        # Remove constant / near-zero variance columns
        if (df.std() < 1e-8).any():
            raise ValueError("One of the columns has near-zero variance after differencing.")

        data = df.values
        safe_lag = min(max_lag, max(1, len(data) // 5))

        if safe_lag < 1:
            raise ValueError("Insufficient data for lag computation.")

        results = grangercausalitytests(
            data, 
            maxlag=safe_lag,
            verbose=False
        )

        p_values = []
        coefficients = []

        for lag in results:
            test_result = results[lag][0]['ssr_ftest']
            p_values.append(test_result[1])  # p-value

            ols_model = results[lag][1][1]
            lag_coefficients = ols_model.params[:-1]  # Exclude the target variable coefficient
            coefficients.append(lag_coefficients)

        min_p_value = min(p_values)
        best_lag = (p_values.index(min_p_value) + 1)

        # Get the coefficient sign for the best lag
        best_coefficients = coefficients[best_lag - 1]
        avg_coefficient = np.mean(best_coefficients[:best_lag])  # average of lag coefficients
        coefficient_sign = "positive" if avg_coefficient > 0 else "negative"

        return {
            "variable": column,
            "best_lag": best_lag,
            "p_value": round(min_p_value, 4),
            "min_p_value": min_p_value,
            "number_of_lags_tested": len(p_values),
            "causal": bool(min_p_value < 0.05),
            "coefficient_sign": coefficient_sign
        }

    def run(self, max_lag: int = 5, error_threshold: float = 0.30) -> dict[dict[str, Any]]:
        if self.columns is None:
            self.columns = [col for col in self.df.columns if col != self.target_column]

        results = []
        for column in self.columns:
            result = self.granger_causality(column, max_lag, error_threshold)
            results.append(result)

        return {
            "causality_test_results": results
        }