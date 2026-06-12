import json
import pandas as pd
from typing import Any, List, Dict, Optional
from dataclasses import dataclass
from tabulate import tabulate

from .base import BaseAnalyzer
from ..utils.mixin import ColumnMixin


@dataclass
class CorrelationParams:
    """
    Parameters for Correlation analysis.

    Attributes:
        columns : Optional[List[str]]
            List of column names to include in the correlation analysis. If None, all numeric columns are used.
        n_lags : int
            Number of lag values to compute for lagged correlation.
        precision : int
            Number of decimal places to round correlation values.
    """
    columns: Optional[List[str]] = None
    n_lags: int = 5
    precision: int = 3


class CorrelationAnalyzer(BaseAnalyzer, ColumnMixin):
    """
    Analyzer for computing correlation matrix and lagged correlations.

    This class computes the correlation matrix for selected columns and the correlation 
    between a lagged version of a column and the original column for specified lags.

    Parameters:
        df : pd.DataFrame
            The input DataFrame containing the data.
        params : CorrelationParams
            The parameters for correlation analysis. 

    Attributes:
        columns : List[str]
            List of column names to include in the correlation analysis.
        n_lags : int
            Number of lag values to compute for lagged correlation.
        precision : int
            Number of decimal places to round correlation values.

    Methods:
        compute() -> Dict[str, Dict]
            Compute the correlation matrix and lagged correlations.
        compute_correlation_matrix() -> Dict[str, Dict[str, float]]
            Compute the correlation matrix for the selected columns.
        compute_lag_correlation() -> Dict[str, Dict[int, float]]
            Compute the correlation between a lagged version of a column and the original column for specified lags.
        print_results_json(results: list[dict] | None, indent: int)
            Print the results in JSON format.
        print_results(results: dict | None)
            Print the results in a human-readable tabular format.
    """

    def __init__(self, df: pd.DataFrame, params: CorrelationParams) -> None:
        super().__init__(df, params)
        self.columns: List[str] = self._get_numeric_columns(params.columns)
        self.n_lags: int = params.n_lags
        self.precision: int = params.precision
        self.corr_matrix: Dict[str, Dict[str, float]] = {}
        self.lag_corr: Dict[str, Dict[int, float]] = {}

    def compute(self) -> Dict[str, Dict]:
        """
        Compute both the correlation matrix and lagged correlations.

        Returns:
            Dict[str, Dict]: A dictionary containing the correlation matrix and lagged correlations.
        """
        corr_matrix = self.compute_correlation_matrix()
        lag_corr = self.compute_lag_correlation()
        return {
            "correlation_matrix": corr_matrix,
            "lagged_correlation_matrix": lag_corr
        }

    def compute_correlation_matrix(self) -> Dict[str, Dict[str, float]]:
        """
        Compute the correlation matrix for the selected columns.

        Returns:
            Dict[str, Dict[str, Dict[str, float]]]: Nested dictionary representing the correlation matrix.
        """
        corr = self.df[self.columns].corr(numeric_only=True).round(self.precision)
        self.corr_matrix = corr.to_dict()
        return self.corr_matrix

    def compute_lag_correlation(self) -> Dict[str, Dict[int, float]]:
        """
        Compute the correlation between a lagged version of a column (t) and the original column (t-lag).

        Returns:
            Dict[str, Dict[int, float]]: Nested dictionary mapping lag values to their corresponding correlation.
        """
        lag_corr: Dict[str, Dict[int, float]] = {}
        for col in self.columns:
            lag_corr[col] = {}
            for lag in range(0, self.n_lags + 1):
                shifted = self.df[col].shift(lag)
                corr = shifted.corr(self.df[col])
                lag_corr[col][lag] = round(corr, self.precision)
        self.lag_corr = lag_corr
        return lag_corr

    def print_results_json(self, results: dict[str, Any] | None = None, indent: int = 2) -> None:
        """
        Print the results in JSON format.

        Args:
            results (dict[str, Any], optional): The results to print. If None, uses the computed correlation and lagged correlation.
            indent (int): The indentation level for pretty-printing the JSON.
        """
        if results is None:
            results = {
                "correlation_matrix": self.corr_matrix,
                "lagged_correlation_matrix": self.lag_corr
            }
        print(json.dumps(results, indent=indent))

    def print_results(self, results: dict[str, Any] | None = None) -> None:
        """
        Print the results in a human-readable tabular format.

        Args:
            results (dict, optional): The results to print. If None, uses the computed correlation and lagged correlation.
        """
        if results is None:
            results = self.compute()

        print("Correlation Matrix:")
        corr_matrix = results.get("correlation_matrix", {})
        if corr_matrix:
            # Convert nested dict to a DataFrame-like structure for tabulate
            corr_df = pd.DataFrame(corr_matrix)
            print(
                tabulate(
                    corr_df.values.tolist(),
                    headers=corr_df.columns.tolist(),
                    tablefmt="simple",
                    floatfmt=f".{self.precision}f",
                )
            )
        else:
            print("No correlation matrix available.")

        print("\nLagged Correlation Matrix:")
        lag_corr = results.get("lagged_correlation_matrix", {})
        if lag_corr:
            # Prepare lagged correlation as a table
            lagged_table = []
            lags = range(0, self.n_lags + 1)
            headers = ["Column"] + [f"Lag {lag}" for lag in lags]
            for col, lag_values in lag_corr.items():
                row = [col] + [lag_values.get(lag, None) for lag in lags]
                lagged_table.append(row)
            print(tabulate(lagged_table, headers=headers, tablefmt='simple', floatfmt=f".{self.precision}f"))
        else:
            print("No lagged correlation matrix available.")