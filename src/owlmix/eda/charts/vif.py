# owlmix/eda/charts/vif.py
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

from owlmix.eda.utils import ColumnMixin


class VIFChart(ColumnMixin):
    def __init__(self, df: pd.DataFrame, target_column: str, features: list[str] = None, precision: int = 2, output_dir: str = "outputs"):
        self.df = df.copy()
        self.target_column = target_column
        self.features = [
            col
            for col in self._get_columns(features)
            if col != target_column
        ]
        self.precision = precision
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

    def add_colors(self) -> list[str]:
        colors = []
        for v in self.vif_df["vif"]:
            if v < 5:
                colors.append("green")
            elif v < 10:
                colors.append("orange")
            else:
                colors.append("red")

        return colors

    def generate(self, filename: str = "vif_chart.png") -> str:
        """
        Generates and saves the VIF bar chart.
        Returns the saved file path.
        """
        _ = self._compute_vif()
        colors = self.add_colors()

        if self.vif_df is None or self.vif_df.empty:
            raise ValueError("VIF DataFrame is empty.")

        # Sort by VIF descending
        df = self.vif_df.sort_values(by="vif", ascending=False)

        plt.figure(figsize=(10, 6))

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

        file_path = os.path.join(self.output_dir, filename)
        plt.savefig(file_path, bbox_inches="tight", dpi=150)
        plt.close()

        return file_path