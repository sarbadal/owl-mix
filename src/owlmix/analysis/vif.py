"""
This module provides classes for calculating the Variance Inflation Factor (VIF) for features in a pandas DataFrame.
VIF is a measure used to detect multicollinearity among explanatory variables in regression analysis.

Classes
-------
- VIFParams: Dataclass for specifying VIF analysis parameters, including the target column, features to analyze,
  precision for VIF values, and optional color thresholds for visualization.
- VIFAnalyzer: Analyzer class that computes VIF values for numeric features, excluding the target column.
  Supports color-coding of VIF values based on user-defined thresholds.

Example
-------
params = VIFParams(
    target_column="y",
    features=["x1", "x2", "x3"],
    color_thresholds=[(5, "orange"), (10, "red")]
)
analyzer = VIFAnalyzer(df, params)
result = analyzer.compute()
# result: {"feature": [...], "vif": [...], "color": [...]}
"""

import json
import pandas as pd
import numpy as np
from dataclasses import dataclass
from tabulate import tabulate
from typing import Dict, Any, List, Optional, Tuple
from statsmodels.stats.outliers_influence import variance_inflation_factor

from .base import BaseAnalyzer
from ..utils.mixin import ColumnMixin


@dataclass
class VIFParams:
    """
    Parameters for VIF analysis.

    Attributes:
        target_column : str
            The name of the target column to exclude from VIF calculation.
        features : Optional[List[str]]
            List of feature column names to include in the analysis. If None, all numeric columns are used.
        precision : int
            Number of decimal places to round VIF values.
        color_thresholds : Optional[List[Tuple[float, str]]]
            List of (threshold, color) tuples for color-coding VIF values. If None, no color-coding is applied.
    """
    target_column: str
    features: Optional[List[str]] = None
    precision: int = 3
    color_thresholds: Optional[List[Tuple[float, str]]] = None


class VIFAnalyzer(BaseAnalyzer, ColumnMixin):
    """
    Analyzer for calculating Variance Inflation Factor (VIF) for features in a DataFrame.

    This class computes VIF values for numeric features, excluding the specified target column.
    Optionally, it can assign colors to VIF values based on user-defined thresholds.

    Parameters:
        df : pd.DataFrame
            The input DataFrame containing the data.
        params : VIFParams
            The parameters for VIF analysis.

    Attributes:
        target_column : str
            The target column to exclude from VIF calculation.
        features : List[str]
            List of feature columns used for VIF calculation.
        precision : int
            Number of decimal places to round VIF values.
        color_thresholds : Optional[List[Tuple[float, str]]]
            Thresholds for color-coding VIF values.

    Methods:
        compute() -> Dict[str, Any]
            Computes VIF values for the specified features and returns a dictionary containing 
            feature names, VIF values, and optional color codes.
        add_colors(vif_values: List[float]) -> List[str]
            Assigns colors to VIF values based on the defined color thresholds.
    """

    def __init__(self, df: pd.DataFrame, params: VIFParams) -> None:
        super().__init__(df, params)
        self.target_column: str = params.target_column
        self.features: List[str] = [
            col
            for col in self._get_numeric_columns(params.features)
            if col != self.target_column
        ]
        self.precision: int = params.precision
        self.color_thresholds: Optional[List[Tuple[float, str]]] = params.color_thresholds

    def add_colors(self, vif_values: List[float]) -> List[str]:
        """
        Assign colors to VIF values based on color thresholds.

        Parameters:
            vif_values : List[float]
                List of VIF values.

        Returns:
            List[str]
                List of color strings corresponding to each VIF value.
        """
        colors: List[str] = []
        for v in vif_values:
            for threshold, color in self.color_thresholds:
                if v < threshold:
                    colors.append(color)
                    break
            else:
                # If no threshold matched, assign the last color
                if self.color_thresholds:
                    colors.append(self.color_thresholds[-1][1])
                else:
                    colors.append("black")
        return colors

    def sort_results_by_vif(self, results: dict) -> dict:
        combined = list(zip(results["feature"], results["vif"], results["color"]))
        combined.sort(key=lambda x: x[1], reverse=True)
        if combined:
            sorted_features, sorted_vifs, sorted_colors = zip(*combined)
            return {
                "feature": list(sorted_features),
                "vif": list(sorted_vifs),
                "color": list(sorted_colors)
            }
        return {
            "feature": [],
            "vif": [],
            "color": []
        }

    def compute(self) -> Dict[str, Any]:
        """
        Compute the VIF values for the selected features.

        Returns:
            Dict[str, Any]
                Dictionary containing:
                    - "feature": List of feature names.
                    - "vif": List of VIF values.
                    - "color": List of color codes for each VIF value (if color_thresholds provided).
        """
        X = self.df[self.features].dropna()
        if X.shape[1] < 2:
            # VIF is not defined for less than 2 features
            return {
                "feature": self.features,
                "vif": [np.nan] * X.shape[1],
                "color": ["black"] * X.shape[1]
            }
        vif_values = [
            round(float(variance_inflation_factor(X.values, i)), self.precision)
            for i in range(X.shape[1])
        ]
        colors = (
            self.add_colors(vif_values)
            if self.color_thresholds else
            ["black"] * len(vif_values)
        )
        results = {
            "feature": self.features,
            "vif": vif_values,
            "color": colors
        }
        return self.sort_results_by_vif(results)

    def print_results_json(self, results: list[dict] = None, indent: int = 2):
        """
        Print the VIF analysis result in JSON format.

        Parameters:
            result : Dict[str, Any]
                The result dictionary returned by the compute() method.
            indent : int
                The number of spaces to use for indentation in the JSON output.
        """
        if results is None:
            results = self.compute()
        print(json.dumps(results, indent=indent))

    def print_results(self, results: dict = None) -> None:
        """
        Prints the VIF results in a readable tabular format.

        Parameters:
            results (dict, optional): Results from ``compute()``. If None, ``compute()`` is called.
        """
        if results is None:
            results = self.compute()
        features = results.get("feature", [])
        vifs = results.get("vif", [])
        colors = results.get("color", [])

        if not features:
            print("No features to display.")
            return

        table = []
        for feat, vif, color in zip(features, vifs, colors):
            table.append([feat, vif, color])
        headers = ["Feature", "VIF", "Color"]
        print(tabulate(table, headers=headers, tablefmt='fancy_grid', floatfmt=f".{self.precision}f"))
        