import json
import pandas as pd
import numpy as np
from dataclasses import dataclass
from statsmodels.tsa.stattools import acf, pacf
from typing import List, Dict, Any

from .base import BaseAnalyzer
from ..utils.mixin import ColumnMixin


@dataclass
class AcfPacfParams:
    """
    Configuration parameters for ACF/PACF analysis.

    Attributes:
        n_lags (int): Number of lags to compute for ACF and PACF.
        precision (int): Decimal places to round the ACF and PACF values.
    """
    columns: List[str] = None
    n_lags: int = 15
    precision: int = 4


class AcfPacfAnalyzer(BaseAnalyzer, ColumnMixin):
    """
    Analyzer to compute ACF and PACF values for numeric columns in a DataFrame.

    Inherits from ColumnMixin to utilize column extraction methods.

    Args:
        df (pd.DataFrame): Input DataFrame containing the time series data.
        columns (List[str], optional): List of column names to analyze. If None, all numeric columns are used.
        params (AcfPacfParams, optional): Configuration parameters for ACF/PACF analysis.

    Methods:
        compute() -> Dict[str, Dict[str, Any]]: Computes ACF and PACF values for the specified columns and returns a dictionary with results.
    """

    def __init__(self, df: pd.DataFrame, params: AcfPacfParams) -> None:
        super().__init__(df, params)
        self.columns = self._get_numeric_columns(params.columns)
        self.n_lags = params.n_lags
        self.precision = params.precision

    def compute(self) -> Dict[str, Dict[str, Any]]:
        """
        Computes ACF and PACF values for the specified columns.

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary where keys are column names and values are dictionaries containing 'acf' and 'pacf' lists.
        """
        results = []
        for col in self.columns:
            series = self.df[col].dropna()
            n_obs = len(series)
            if n_obs < self.n_lags + 1:
                raise ValueError(
                    f"Column '{col}' has only {n_obs} observations, which is less than the "
                    f"required {self.n_lags + 1} for ACF/PACF computation."
                )
            if not np.issubdtype(series.dtype, np.number):
                continue  # Skip non-numeric columns

            acf_values = acf(series, nlags=self.n_lags, fft=False)
            pacf_values = pacf(series, nlags=self.n_lags)
            lags = list(range(len(acf_values)))
            results.append({
                "column": col,
                "n_obs": n_obs,
                "lags": lags,
                "acf": np.round(acf_values, self.precision).tolist(),
                "pacf": np.round(pacf_values, self.precision).tolist()
            })
        return results

    def print_results_json(self, results: list[dict] = None, indent: int = 2) -> None:
        """
        Prints the ACF and PACF results as pretty-formatted JSON.
        Args:
            results (list, optional): Results from ``compute()``. If None, ``compute()`` is called.
            indent (int): Number of spaces for indentation in JSON output.
        """
        if results is None:
            results = self.compute()
        print(json.dumps(results, indent=indent))

    def print_results(self, results: list[dict] = None) -> None:
        """
        Prints the ACF and PACF results in a readable format.
        Args:
            results (list, optional): Results from ``compute()``. If None, ``compute()`` is called.
        """
        if results is None:
            results = self.compute()
        for res in results:
            print(f"\nColumn: {res['column']} (n_obs={res['n_obs']})")
            print("Lag |   ACF   |  PACF")
            print("-" * 25)
            for lag, acf_val, pacf_val in zip(res['lags'], res['acf'], res['pacf']):
                print(f"{lag:>3} | {acf_val:>7} | {pacf_val:>7}")

    
