# src/owlmix/eda/correlation.py
import json 
import pandas as pd

from .utils import to_json
 
 
def get_correlation_matrix(df: pd.DataFrame) -> dict:
    corr = df.corr(numeric_only=True)
    return json.dumps(corr.to_dict(), indent=2)
 
 
def get_lag_correlation(df: pd.DataFrame, column: str, target: str, lags: list[int]) -> dict[int, float]:
    results = {}
 
    for lag in lags:
        lagged = df[column].shift(lag)
        corr = lagged.corr(df[target])
        results[lag] = corr
 
    return json.dumps(results, indent=2)


class Correlation:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.corr_matrix = None
        self.lag_corr = None
 
    def compute_correlation_matrix(self) -> dict:
        corr = self.df.corr(numeric_only=True)
        self.corr_matrix = corr.to_dict()
        return self.corr_matrix
 
    def compute_lag_correlation(self, column: str, target: str, lags: list[int]) -> dict[int, float]:
        results = {}
 
        for lag in lags:
            lagged = self.df[column].shift(lag)
            corr = lagged.corr(self.df[target])
            results[lag] = corr
 
        self.lag_corr = results
        return self.lag_corr

    def compute(self, column: str, target: str, lags: list[int]) -> dict:
        self.compute_correlation_matrix()
        self.compute_lag_correlation(column, target, lags)
        return {
            "correlation_matrix": self.corr_matrix,
            "lag_correlation": self.lag_corr
        }
 
    def to_json(self, column: str, target: str, lags: list[int]) -> str:
        """Get the correlation results as a JSON string."""
        if self.corr_matrix is None or self.lag_corr is None:
            self.compute(column, target, lags)
        return to_json(self.result)