import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, List, Callable, Optional, Any


class BaseResponseCurve(ABC):
    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series):
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> pd.Series:
        pass


class LinearResponseCurve(BaseResponseCurve):
    def __init__(self):
        self.coef_ = None
        self.intercept_ = None
        self.feature_columns_ = None

    def fit(self, X: pd.DataFrame, y: pd.Series):
        self.feature_columns_ = X.columns.tolist()
        X_matrix = X.values
        y_vector = y.values
        ones = np.ones((X_matrix.shape[0], 1))
        X_design = np.hstack((ones, X_matrix))
        beta = np.linalg.inv(X_design.T @ X_design) @ X_design.T @ y_vector
        self.intercept_ = float(beta[0])
        self.coef_ = beta[1:].flatten()

    def predict(self, X: pd.DataFrame) -> pd.Series:
        if self.coef_ is None or self.intercept_ is None:
            raise ValueError("Model is not fitted yet.")
        X_matrix = X[self.feature_columns_].values
        predictions = self.intercept_ + X_matrix @ self.coef_
        return pd.Series(predictions, index=X.index)


class NonLinearResponseCurve(BaseResponseCurve):
    def __init__(self, transformation: Callable[[pd.DataFrame], pd.DataFrame]):
        self.transformation = transformation
        self.linear_model = LinearResponseCurve()

    def fit(self, X: pd.DataFrame, y: pd.Series):
        transformed_X = self.transformation(X)
        self.linear_model.fit(transformed_X, y)

    def predict(self, X: pd.DataFrame) -> pd.Series:
        transformed_X = self.transformation(X)
        return self.linear_model.predict(transformed_X)


def hill(x: np.ndarray, alpha: float, gamma: float, c: float = 1.0) -> np.ndarray:
    """
    Hill function for modeling nonlinear response curves.
    
    Parameters:
    - x: Input values.
    - alpha: Maximum response.
    - gamma: Hill coefficient (controls the steepness of the curve).
    - c: Half-maximal effective concentration (EC50).

    Returns:
    - np.ndarray: Output values of the Hill function.
    """
    return (x ** gamma) / (alpha ** gamma + x ** gamma)

def adstock(x: np.ndarray, decay_rate: float) -> np.ndarray:
    """
    Adstock transformation for modeling delayed effects in response curves.
    
    Parameters:
    - x: Input values (e.g., advertising spend).
    - decay_rate: Rate at which the effect decays over time (0 < decay_rate < 1).

    Returns:
    - np.ndarray: Output values of the Adstock transformation.
    """
    result = np.zeros_like(x)
    for i in range(len(x)):
        result[i] = x[i] + decay_rate * (result[i-1] if i > 0 else 0)
    return result


@dataclass
class ResponseCurveConfig:
    model_type: str = "linear"
    feature_columns: Optional[List[str]] = None
    target_column: Optional[str] = None
    time_column: Optional[str] = None
    transformations: Optional[Dict[str, Callable]] = None
    baseline: Optional[str] = "mean"


class ResponseCurveAnalyzer:
    def __init__(self, df: pd.DataFrame, params: ResponseCurveConfig):
        self.df = df
        self.params = params
        self.model = self._model_selector()

    def _model_selector(self) -> BaseResponseCurve:
        model_mapping = {
            "linear": LinearResponseCurve,
            "nonlinear": lambda: NonLinearResponseCurve(transformation=self.params.transformations)
        }
        model_class = model_mapping.get(self.params.model_type.lower())
        if model_class is None:
            raise ValueError(f"Unsupported model type: {self.params.model_type}")
        return model_class()

    def _compute_baseline(self) -> Dict[str, float]:
        baseline_values = {}
        for feature in self.params.feature_columns:
            if self.params.baseline == "mean":
                baseline_values[feature] = self.df[feature].mean()
                return baseline_values
            if self.params.baseline == "median":
                baseline_values[feature] = self.df[feature].median()
                return baseline_values
            baseline_values[feature] = 0.0
            return baseline_values

    def _apply_transformation(self, feature: str, values: np.ndarray) -> np.ndarray:
        if self.params.transformations and feature in self.params.transformations:
            return self.params.transformations[feature](values)
        return values

    def _predict(self, df_row: pd.DataFrame) -> float:
        return float(self.model.predict(df_row[self.params.feature_columns])[0])

    def generate_response_curve_json(self, feature: str, num_points: int = 100, value_range: Optional[Tuple[float, float]] = None) -> Dict[str, Any]:
        if feature not in self.params.feature_columns:
            raise ValueError(f"Feature '{feature}' is not in the list of feature columns.")
        baseline_values = self._compute_baseline()
        min_value = value_range[0] if value_range else self.df[feature].min()
        max_value = value_range[1] if value_range else self.df[feature].max()
        test_values = np.linspace(min_value, max_value, num_points)
        input_values, predictions = [], []
        for value in test_values:
            row = {col: baseline_values.get(col, self.df[col].mean()) for col in self.params.feature_columns}
            row[feature] = value
            df_row = pd.DataFrame([row])
            for col in self.params.feature_columns:
                df_row[col] = self._apply_transformation(col, df_row[col].values)
            pred = self._predict(df_row)
            input_values.append(value)
            predictions.append(pred)

        return {
            "feature": feature, 
            "input_values": input_values, 
            "predictions": predictions
        }

    def generate_all_response_curves_json(self, num_points: int = 100) -> Dict[str, Any]:
        response_curves = []
        for feature in self.params.feature_columns:
            response_curves.append(self.generate_response_curve_json(feature, num_points))
        return response_curves


if __name__ == "__main__":    # Example usage
    data = {
        "feature1": [1, 2, 3, 4, 5],
        "feature2": [2, 3, 4, 5, 6],
        "target": [1, 2, 3, 4, 5]
    }
    df = pd.DataFrame(data)
    params = ResponseCurveConfig(
        model_type="linear",
        feature_columns=["feature1", "feature2"],
        target_column="target",
        transformations={
            "feature1": lambda x: np.log(x + 1),
            "feature2": hill
        },
        baseline="mean"
    )
    analyzer = ResponseCurveAnalyzer(df, params)
    response_curves_json = analyzer.generate_all_response_curves_json()
    print(response_curves_json)
