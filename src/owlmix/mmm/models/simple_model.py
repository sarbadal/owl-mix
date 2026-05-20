import numpy as np

class SimpleLinearModel:
    def __init__(self, coefficients: dict, intercept: float = 0.0):
        self.coefficients = coefficients
        self.intercept = intercept

    def predict(self, X):
        preds = []
        for _, row in X.iterrows():
            y = self.intercept
            for col, coef in self.coefficients.items():
                y += coef * row[col]
            preds.append(y)
        return np.array(preds)
