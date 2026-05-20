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
        if self.func_type == "exponential":
            func = self._exp_func
            initial_guess = [max(y), 0.001]
 
        elif self.func_type == "logistic":
            func = self._logistic_func
            initial_guess = [max(y), 0.01, np.median(x)]
 
        else:
            raise ValueError("Unsupported function type")
 
        params, _ = curve_fit(func, x, y, p0=initial_guess, maxfev=10000)
        self.params = params
        self.func = func
 
    def predict(self, x):
        if self.params is None:
            raise ValueError("Model not fitted yet")
        return self.func(x, *self.params)
 