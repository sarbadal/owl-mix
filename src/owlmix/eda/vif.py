
import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

from owlmix.eda.utils import ColumnMixin


class VIFCalculator(ColumnMixin):
    def __init__(self, df: pd.DataFrame, target_column: str, features: list[str] = None, precision: int = 2):
        self.df = df.copy()
        self.target_column = target_column
        self.features = [
            col
            for col in self._get_columns(features)
            if col != target_column
        ]
        self.precision = precision

    def compute_vif(self) -> dict:
        X = self.df[self.features].dropna()
        vif_data = {
            "feature": self.features,
            "vif_value": [
                round(variance_inflation_factor(X.values, i), self.precision)
                for i in range(X.shape[1])
            ],
        }
        return vif_data
