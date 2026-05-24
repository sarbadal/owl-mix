import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_is_fitted
from typing import Self


class SimpleLinearModelSK(BaseEstimator, RegressorMixin):
    """
    Scikit-learn compatible linear model:
    - If coefficients are provided, uses them.
    - If not, fits coefficients using least squares.
    """

    def __init__(self, coefficients: dict = None, intercept: float = 0.0):
        self.coefficients = coefficients
        self.intercept = intercept

    def fit(self, X: pd.DataFrame, y: pd.Series) -> Self:
        self._validate_inputs(X, y)
        self.feature_names_in_ = np.array(X.columns, dtype=object)

        if self.coefficients is None:
            return self._fit_from_data(X, y)

        return self._fit_from_params()

    def _fit_from_params(self) -> Self:
        self.intercept_ = float(self.intercept)
        self.coefficients_ = self.coefficients
        return self

    def _fit_from_data(self, X, y) -> Self:
        X_clean, y_clean = self._prepare_data(X, y)
        self._solve_least_squares(X_clean, y_clean, X.columns)
        return self

    def _validate_inputs(self, X, y):
        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be a pandas DataFrame.")
        if not isinstance(y, pd.Series):
            raise TypeError("y must be a pandas Series.")

    def _prepare_data(self, X: pd.DataFrame, y: pd.Series) -> tuple[np.ndarray, np.ndarray]:
        # Coerce to numeric and filter finite rows
        X_arr = X.apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
        y_arr = pd.to_numeric(y, errors="coerce").to_numpy(dtype=float).flatten()

        if X_arr.ndim != 2 or X_arr.shape[0] != y_arr.shape[0]:
            raise ValueError("Shape mismatch between X and y.")

        mask = np.isfinite(X_arr).all(axis=1) & np.isfinite(y_arr)
        X_clean, y_clean = X_arr[mask], y_arr[mask]

        if X_clean.shape[0] <= X_clean.shape[1]:
            raise ValueError("Not enough valid rows to fit model.")
            
        return X_clean, y_clean

    def _solve_least_squares(self, X: pd.DataFrame, y: pd.Series, columns: list[str]):
        # Add constant for intercept
        X_design = np.column_stack([np.ones(X.shape[0]), X])
        
        try:
            coef, *_ = np.linalg.lstsq(X_design, y, rcond=None)
            self.intercept_ = float(coef[0])
            self.coefficients_ = dict(zip(columns, coef[1:]))
        except np.linalg.LinAlgError as e:
            raise ValueError("Linear least squares failed to converge.") from e

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        check_is_fitted(self, attributes=["intercept_", "coefficients_"])

        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be a pandas DataFrame with named columns.")

        missing = [c for c in self.coefficients_ if c not in X.columns]
        if missing:
            raise ValueError(f"Missing required columns in X: {missing}")

        X_used = X[list(self.coefficients_.keys())].apply(pd.to_numeric, errors="coerce")
        X_arr = X_used.to_numpy(dtype=float)

        if not np.isfinite(X_arr).all():
            raise ValueError("X contains NaN or inf values in required feature columns.")

        coef_arr = np.array([self.coefficients_[c] for c in X_used.columns], dtype=float)
        y = self.intercept_ + X_arr @ coef_arr
        return y