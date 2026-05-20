import numpy as np
from .base import BaseTransformer

class LogTransformer(BaseTransformer):
    def __init__(self, epsilon=1e-8):
        self.epsilon = epsilon

    def transform(self, x):
        x = np.array(x)
        return np.log(x + self.epsilon)