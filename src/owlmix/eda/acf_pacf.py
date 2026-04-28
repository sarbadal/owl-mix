# owlmix/eda/acf_pacf.py
"""
Provides the ACFPACFCalculator class for computing the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF)
for specified columns in a pandas DataFrame. Utilizes statsmodels for time series analysis and supports configurable lag and precision.

Classes:
    ACFPACFCalculator: Calculates ACF and PACF values for given DataFrame columns.

Example:
    calculator = ACFPACFCalculator(df, columns=["col1", "col2"])
    result = calculator.generate()
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import acf, pacf
from typing import List, Dict, Any

from .utils import ColumnMixin

ACFPACFResult = Dict[str, Any]


class ACFPACFCalculator(ColumnMixin):
    """
    Calculates the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF)
    for specified columns in a pandas DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing time series data.
        columns (list[str]): List of column names to compute ACF/PACF for.
        n_lags (int, optional): Number of lags to compute. Defaults to 15.
        precision (int, optional): Decimal precision for results. Defaults to 3.
    """
    def __init__(self, df: pd.DataFrame, columns: list[str], n_lags: int = 15, precision: int = 3) -> None:
        self.df = df.copy()
        self.columns = self._get_columns(columns)
        self.n_lags = n_lags
        self.precision = precision

    def generate(self) -> ACFPACFResult:
        """
        Calculate ACF and PACF for each specified column.

        Returns:
            dict[str, list[dict]]: A dictionary with a "data" key containing a 
            list of results for each column.
        """
        results: List[ACFPACFResult] = []

        for col in self.columns:
            series = self.df[col].dropna()
            n_obs = len(series)

            if not np.issubdtype(series.dtype, np.number):
                continue  # or raise an error

            # Compute ACF & PACF
            acf_vals = acf(series, nlags=self.n_lags)
            pacf_vals = pacf(series, nlags=self.n_lags)
            lags = list(range(len(acf_vals)))

            results.append({
                "column": col,
                "n_obs": n_obs,
                "lags": lags,
                "acf": np.round(acf_vals, self.precision).tolist(),
                "pacf": np.round(pacf_vals, self.precision).tolist()
            })

        return {
            "data": results
        }