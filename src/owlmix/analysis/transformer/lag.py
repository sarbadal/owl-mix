import pandas as pd

from .base import BaseTransformer


class LagTransformer(BaseTransformer):

    def __init__(self, lag: int = 1):
        self.lag = lag

    def transform(self, series: pd.Series) -> pd.Series:
        return series.shift(self.lag)