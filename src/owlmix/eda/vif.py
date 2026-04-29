# owlmix/eda/vif.py
import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

from .utils import ColumnMixin


class VIFCalculator(ColumnMixin):
    """
    Calculates Variance Inflation Factor (VIF) for features in a DataFrame.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        target_column: str,
        features: Optional[List[str]] = None,
        precision: int = 2
    ):
        """
        Initialize the VIFCalculator.

        Args:
            df (pd.DataFrame): Input DataFrame.
            target_column (str): The target column to exclude from VIF calculation.
            features (Optional[List[str]]): List of features to include. If None, all columns except target are used.
            precision (int): Decimal precision for VIF values.
        """
        self.df = df.copy()
        self.target_column = target_column
        self._features = features
        self.precision = precision

    @property
    def features(self) -> List[str]:
        """
        Returns the list of features used for VIF calculation, excluding the target column.
        """
        return [
            col for col in self._get_columns(self._features)
            if col != self.target_column
        ]

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
        return {"feature": self.features, "vif_value": vif_values}
