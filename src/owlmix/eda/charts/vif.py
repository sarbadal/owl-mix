# owlmix/eda/charts/vif.py
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import TypedDict, NotRequired, Unpack
from statsmodels.stats.outliers_influence import variance_inflation_factor

from ..utils import ColumnMixin
from ..args.vif import SetVIFConfigArgs


class VIFChart(ColumnMixin):
    def __init__(self, df: pd.DataFrame, output_dir: str = "charts", **config: Unpack[SetVIFConfigArgs]):
        self.df = df.copy()
        self.target_column = config.get("target_column")
        self.features = config.get("features")
        self.features = [
            col
            for col in self._get_columns(config.get("features", None))
            if col != self.target_column
        ]
        self.precision = config.get("precision", 3)
        self.color_thresholds = config.get("color_thresholds", None)
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

    def _compute_vif(self) -> pd.DataFrame:
        X = self.df[self.features].dropna()
        vif_data = {
            "feature": self.features,
            "vif": [
                round(variance_inflation_factor(X.values, i), self.precision)
                for i in range(X.shape[1])
            ],
        }
        self.vif_df = pd.DataFrame(vif_data)
        return self.vif_df

    def add_colors(self, df: pd.DataFrame) -> list[str]:
        colors = []
        for v in df["vif"]:
            for threshold, color in self.color_thresholds:
                if v < threshold:
                    colors.append(color)
                    break
        return colors

    def generate(self) -> str:
        """
        Generates and saves the VIF bar chart.
        Returns the saved file path.
        """
        _ = self._compute_vif()

        if self.vif_df is None or self.vif_df.empty:
            raise ValueError("VIF DataFrame is empty.")

        # Sort by VIF descending
        df = self.vif_df.sort_values(by="vif", ascending=False)
        colors = self.add_colors(df)  # Add colors based on thresholds based on the sorted VIF values

        plt.figure(figsize=(12, 6))

        plt.barh(df["feature"], df["vif"], color=colors)
        plt.gca().invert_yaxis() # highest VIF on top

        # Threshold lines
        plt.axvline(x=5, linestyle="--")
        plt.axvline(x=10, linestyle="--")

        plt.xlabel("VIF Value")
        plt.ylabel("Feature")
        plt.title("Variance Inflation Factor (VIF)")

        for i, v in enumerate(df["vif"]):
            plt.text(v, i, f"{v:.2f}", va='center', ha='center', fontsize=10)

        plt.tight_layout()

        file_path = os.path.join(self.output_dir, "vif_chart.png")
        plt.savefig(file_path, bbox_inches="tight", dpi=150)
        plt.close()

        return file_path