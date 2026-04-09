# src/owlmix/eda/analyzer.py
 
import pandas as pd
from .stats import get_basic_stats
from .correlation import get_correlation_matrix, get_lag_correlation
from .summary import SummaryBuilder
 
 
class EDAAnalyzer:
    def __init__(self, df: pd.DataFrame, target: str | None = None):
        self.df = df.copy()
        self.target = target
 
    def basic_stats(self) -> pd.DataFrame:
        return get_basic_stats(self.df)
 
    def correlation(self) -> pd.DataFrame:
        return get_correlation_matrix(self.df)
 
    def lag_correlation(self, column: str, lags: list[int]):
        if not self.target:
            raise ValueError("Target variable must be provided for lag correlation.")
        return get_lag_correlation(self.df, column, self.target, lags)
 
    def summary(self) -> str:
        builder = SummaryBuilder(self.df, self.target)
 
        builder.add_basic_info()
        builder.add_missing_summary()
        builder.add_descriptive_stats()
        builder.add_correlation()
 
        return builder.build()