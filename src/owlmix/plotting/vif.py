import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack
from statsmodels.stats.outliers_influence import variance_inflation_factor

from .base import BasePlotter

@dataclass
class VIFPlotParams:
    ...


class VIFPlotter(BasePlotter):

    def __init__(self, data: pd.DataFrame, params: VIFPlotParams = VIFPlotParams):
        super().__init__(data, params)

    def generate(self, output_dir: str = "outputs/charts") -> str:
        plt.figure(figsize=(12, 6))
        plt.barh(self.data["feature"], self.data["vif"], color=self.data["color"])
        plt.gca().invert_yaxis()  # Invert y-axis to have the highest VIF on top

        plt.axvline(x=5, linestyle="--")
        plt.axvline(x=10, linestyle="--")

        plt.xlabel("VIF Value")
        plt.ylabel("Feature")
        plt.title("Variance Inflation Factor (VIF)")

        for i, v in enumerate(self.data["vif"]):
            plt.text(v, i, f"{v:.2f}", va='center', ha='center', fontsize=10)
        plt.tight_layout()

        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, "vif_chart.png")
        plt.savefig(file_path, bbox_inches="tight", dpi=150)
        plt.close()

        return file_path