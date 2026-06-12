import os
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Any

from .base import BasePlotter

@dataclass
class VIFPlotParams:
    ...


class VIFPlotter(BasePlotter):

    def __init__(self, data: dict[str, Any], params: VIFPlotParams | None = None):
        super().__init__(data, params or VIFPlotParams())

    def generate(self, output_dir: str = "outputs/charts") -> str:
        plt.figure(figsize=(12, 8))
        plt.barh(self.data["feature"], self.data["vif"], color=self.data["color"])
        ax = plt.gca()
        ax.invert_yaxis()

        plt.axvline(x=5, linestyle="--")
        plt.axvline(x=10, linestyle="--")

        ax.set_xlabel("VIF Value", fontsize=18)
        ax.set_ylabel("Feature", fontsize=18)
        ax.set_title("Variance Inflation Factor (VIF)", fontsize=20)

        # tick label size for both x and y axis
        ax.tick_params(axis="both", labelsize=16)

        for i, v in enumerate(self.data["vif"]):
            ax.text(v, i, f"{v:.2f}", va="center", ha="center", fontsize=16)

        plt.tight_layout()

        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, "vif_chart.png")
        plt.savefig(file_path, bbox_inches="tight", dpi=150)
        plt.close()
        return file_path