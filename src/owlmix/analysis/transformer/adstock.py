import pandas as pd 
import numpy as np
from enum import Enum

from .base import BaseTransformer


class AdstockMethod(str, Enum):
    GEOMETRIC = "geometric"


class AdstockTransformer(BaseTransformer):
    def __init__(self, lag: int = 0, method: AdstockMethod = AdstockMethod.GEOMETRIC, decay_rate: float = 0.5):
        self.lag = lag
        self.method = method
        self.decay_rate = decay_rate

    def transform(self, series: pd.Series) -> pd.Series:
        series = series.copy()
        series = series.shift(self.lag)
        if self.method == AdstockMethod.GEOMETRIC:
            return self._geometric(series)
        raise ValueError(f"Unknown adstock method: {self.method}")

    def _geometric(self, series: pd.Series) -> pd.Series:
        series = series.copy()
        result = np.zeros_like(series)
        result[0] = series.iloc[0]
        for t in range(1, len(series)):
            result[t] = series.iloc[t] + self.decay_rate * result[t - 1]
        return pd.Series(result, index=series.index)