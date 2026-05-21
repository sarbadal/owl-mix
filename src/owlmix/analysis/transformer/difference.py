import pandas as pd

from .base import BaseTransformer

class DifferenceTransformer(BaseTransformer):
    def __init__(self, period: int = 1, lag: int = 0):
        self.period = period
        self.lag = lag

    def transform(self, series: pd.Series) -> pd.Series:
        series = series.copy()
        series = series.shift(self.lag) if self.lag > 0 else series
        return series.diff(self.period).fillna(0)