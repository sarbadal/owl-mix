# owlmix/eda/vif.py
import pandas as pd
import numpy as np
from typing import Unpack, Dict, Any
from statsmodels.stats.outliers_influence import variance_inflation_factor

from .utils import ColumnMixin
from .args.vif import SetVIFConfigArgs


class VIFCalculator(ColumnMixin):
    """
    Calculates Variance Inflation Factor (VIF) for features in a DataFrame.
    """

    def __init__(self, df: pd.DataFrame, **config: Unpack[SetVIFConfigArgs]):
        """
        Initialize the VIFCalculator.

        Args:
            df (pd.DataFrame): Input DataFrame.
            target_column (str): The target column to exclude from VIF calculation.
            features (Optional[List[str]]): List of features to include. If None, all columns except target are used.
            precision (int): Decimal precision for VIF values.
        """
        self.df = df.copy()
        self.target_column = config.get("target_column", None)
        self.features = [
            col
            for col in self._get_columns(config.get("features", None))
            if col != self.target_column
        ]
        self.precision = config.get("precision", 3)
        self.color_thresholds = config.get("color_thresholds", None)

    def add_colors(self, vif_values: list[float]) -> list[str]:
        colors = []
        for v in vif_values:
            for threshold, color in self.color_thresholds:
                if v < threshold:
                    colors.append(color)
                    break
        return colors

    def compute_vif(self) -> Dict[str, Any]:
        """
        Compute VIF for the features.

        Returns:
            Dict[str, Any]: Dictionary with 'feature' and 'vif_value' lists.
        """
        X = self.df[self.features].dropna()
        if X.shape[1] < 2:
            # VIF is not defined for less than 2 features
            return {"feature": self.features, "vif_value": [np.nan] * X.shape[1]}
        vif_values = [
            round(variance_inflation_factor(X.values, i), self.precision)
            for i in range(X.shape[1])
        ]
        colors = self.add_colors(vif_values) if self.color_thresholds else ["black"] * len(vif_values)
        return {
            "feature": self.features, 
            "vif_value": vif_values, 
            "color": colors
        }
