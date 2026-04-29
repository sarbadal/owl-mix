# owlmix/eda/correlation.py
import pandas as pd
from typing import List, Optional, Dict, Any

from .utils import to_json, ColumnMixin

class Correlation(ColumnMixin):
    """
    Provides methods to compute correlation matrices and lagged correlations for a DataFrame.
    """

    def __init__(self, df: pd.DataFrame, columns: Optional[List[str]] = None):
        """
        Initialize the Correlation object.

        Args:
            df (pd.DataFrame): The input DataFrame.
            columns (Optional[List[str]]): List of columns to consider for correlation. If None, uses all columns.
        """
        self.df = df.copy()
        self.columns = self._get_columns(columns)
        self.corr_matrix: Optional[Dict[str, Dict[str, float]]] = None
        self.lag_corr: Optional[Dict[int, float]] = None

    def compute_correlation_matrix(self) -> Dict[str, Dict[str, float]]:
        """
        Compute the correlation matrix for the selected columns.

        Returns:
            Dict[str, Dict[str, float]]: Nested dictionary representing the correlation matrix.
        """
        corr = self.df[self.columns].corr(numeric_only=True)
        self.corr_matrix = corr.to_dict()
        return self.corr_matrix

    def compute_lag_correlation(self, column: str, target: str, lags: List[int]) -> Dict[int, float]:
        """
        Compute the correlation between a lagged version of a column and a target column for given lags.

        Args:
            column (str): The column to lag.
            target (str): The target column to correlate with.
            lags (List[int]): List of lag values.

        Returns:
            Dict[int, float]: Dictionary mapping lag to correlation value.
        """
        results = {}
        for lag in lags:
            lagged = self.df[column].shift(lag)
            corr = lagged.corr(self.df[target])
            results[lag] = corr
        self.lag_corr = results
        return self.lag_corr

    def compute(self, column: str, target: str, lags: List[int]) -> Dict[str, Any]:
        """
        Compute both the correlation matrix and lagged correlations.

        Args:
            column (str): The column to lag.
            target (str): The target column to correlate with.
            lags (List[int]): List of lag values.

        Returns:
            Dict[str, Any]: Dictionary with 'correlation_matrix' and 'lag_correlation' results.
        """
        corr_matrix = self.compute_correlation_matrix()
        lag_corr = self.compute_lag_correlation(column, target, lags)
        return {
            "correlation_matrix": corr_matrix,
            "lag_correlation": lag_corr
        }

    def to_json(self, column: str, target: str, lags: List[int]) -> str:
        """
        Get the correlation results as a JSON string.

        Args:
            column (str): The column to lag.
            target (str): The target column to correlate with.
            lags (List[int]): List of lag values.

        Returns:
            str: JSON string of the results.
        """
        result = self.compute(column, target, lags)
        return to_json(result)