import numpy as np
from scipy.optimize import curve_fit
 
 
class SCurveFitter:
    def __init__(self, func_type="exponential"):
        self.func_type = func_type
        self.params = None
 
    def _exp_func(self, x, a, b):
        return a * (1 - np.exp(-b * x))
 
    def _logistic_func(self, x, L, k, x0):
        return L / (1 + np.exp(-k * (x - x0)))

    def fit(self, x, y):
        registry = {
            "exponential": (self._exp_func, [max(y), 0.001]),
            "logistic": (self._logistic_func, [max(y), 0.01, np.median(x)]),
            # Additional functions can be added here
        }

        if self.func_type not in registry:
            raise ValueError(f"Unsupported function type: {self.func_type}")

        self.func, initial_guess = registry[self.func_type]
        params, _ = curve_fit(self.func, x, y, p0=initial_guess, maxfev=10000)
        self.params = params
 
    def predict(self, x):
        if self.params is None:
            raise ValueError("Model not fitted yet")
        return self.func(x, *self.params)
 