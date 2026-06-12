import numpy as np
from typing import Self
from .base import BaseTransformer

class MinMaxScaler(BaseTransformer):
    def fit(self, x: np.ndarray) -> Self:
        x = np.array(x)
        self.min_ = x.min()
        self.max_ = x.max()
        return self

    def transform(self, x: np.ndarray) -> np.ndarray:
        x = np.array(x)
        return (x - self.min_) / (self.max_ - self.min_ + 1e-8)