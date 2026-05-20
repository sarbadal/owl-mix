import numpy as np
from .base import BaseTransformer

class HillTransformer(BaseTransformer):
    def __init__(self, alpha=50, gamma=1.5):
        self.alpha = alpha
        self.gamma = gamma

    def transform(self, x):
        x = np.asarray(x, dtype=float)
        if self.alpha <= 0:
            raise ValueError("alpha must be > 0 for Hill transformation")
        if self.gamma <= 0:
            raise ValueError("gamma must be > 0 for Hill transformation")

        x_pos = np.clip(x, 0.0, None)
        x_pow = np.power(x_pos, self.gamma)
        a_pow = float(self.alpha) ** self.gamma
        denom = a_pow + x_pow
        return np.divide(x_pow, denom, out=np.zeros_like(x_pow), where=denom != 0)