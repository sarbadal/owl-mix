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
        X = X.copy()

        if not isinstance(X, pd.DataFrame):
            raise TypeError("X must be a pandas DataFrame with named columns.")

        if not isinstance(y, pd.Series):
            raise TypeError("y must be a pandas Series.")

        # Keep sklearn-style feature metadata from original columns.
        self.feature_names_in_ = np.array(list(X.columns), dtype=object)

        if self.coefficients is None:
            # Coerce to numeric; invalid parses become NaN and are filtered out.
            X_num = X.apply(pd.to_numeric, errors="coerce")
            y_num = pd.to_numeric(y, errors="coerce")

            X_arr = X_num.to_numpy(dtype=float)
            y_arr = np.asarray(y_num, dtype=float)

            if X_arr.ndim != 2:
                raise ValueError("X must be 2D.")
            if y_arr.ndim != 1:
                y_arr = y_arr.reshape(-1)
            if X_arr.shape[0] != y_arr.shape[0]:
                raise ValueError(
                    f"X and y must have same number of rows. Got {X_arr.shape[0]} and {y_arr.shape[0]}."
                )

            finite_mask = np.isfinite(X_arr).all(axis=1) & np.isfinite(y_arr)
            if not finite_mask.any():
                raise ValueError(
                    "No valid rows to fit after removing NaN/inf values from X and y."
                )

            X_clean = X_arr[finite_mask]
            y_clean = y_arr[finite_mask]

            if X_clean.shape[0] <= X_clean.shape[1]:
                raise ValueError(
                    "Not enough valid rows to fit a stable linear model after filtering NaN/inf values."
                )

            X_design = np.hstack([np.ones((X_clean.shape[0], 1), dtype=float), X_clean])

            try:
                coef, *_ = np.linalg.lstsq(X_design, y_clean, rcond=None)
            except np.linalg.LinAlgError as e:
                raise ValueError(
                    "Linear least squares failed to converge. "
                    "Check for extreme scaling, collinearity, or remaining invalid values."
                ) from e

            self.intercept_ = float(coef[0])
            self.coefficients_ = dict(zip(X.columns, coef[1:]))
        else:
            self.intercept_ = float(self.intercept)
            self.coefficients_ = self.coefficients

        return self

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