import numpy as np
from .base import BaseTransformer

class AdstockTransformer(BaseTransformer):
    def __init__(self, decay=0.5):
        self.decay = decay

    def transform(self, x: np.ndarray) -> np.ndarray:
        x = np.array(x)
        result = np.zeros_like(x, dtype=float)
        result[0] = x[0]
        for t in range(1, len(x)):
            result[t] = x[t] + self.decay * result[t - 1]
        return result
