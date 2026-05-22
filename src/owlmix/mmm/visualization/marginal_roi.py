import os
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from typing import Any, Dict, Optional, Tuple


@dataclass
class MarginalROIPlotConfig:
    line_color: str = "#1f77b4"  # blue
    fitted_line_color: str = "#ff7f0e"  # orange
    label_color: str = "#888888"  # neutral gray
    font_size: int = 16


class MarginalROIPlotter:
    """Plots marginal ROI curve with optional fitted curve and saves the chart as a PNG file."""
    def __init__(self, curve: Dict, classification: Dict, params: MarginalROIPlotConfig = MarginalROIPlotConfig):
        self.curve = curve
        self.classification = classification
        self.params = params

    def plot(self, output_dir: str = "outputs/charts") -> str:
        x = self.curve["input_value"]
        y = self.classification["marginal"]

        plt.figure()
        plt.plot(
            x, y, label="Marginal ROI",
            color=self.params.line_color,
            alpha=0.95,
            linewidth=3  # Increased thickness
        )

        if "fitted_curve" in self.curve:
            plt.plot(
                x,
                self.curve["fitted_curve"],
                linestyle="--",
                label="Fitted Curve",
                color=self.params.fitted_line_color,
                alpha=0.95,
                linewidth=3  # Increased thickness
            )

        label_color = self.params.label_color
        plt.xlabel(self.curve["feature"], color=label_color, fontsize=self.params.font_size)
        plt.ylabel("Marginal ROI", color=label_color, fontsize=self.params.font_size)
        plt.legend(fontsize=self.params.font_size)
        plt.tight_layout()

        ax = plt.gca()
        ax.tick_params(colors=label_color, labelsize=self.params.font_size)  # Set tick label size
        for spine in ax.spines.values():
            spine.set_color(label_color)

        formatter = FuncFormatter(lambda x, _: f'{int(x/1000)}K' if abs(x) >= 1000 else f'{int(x)}')
        ax.xaxis.set_major_formatter(formatter)
        ax.yaxis.set_major_formatter(formatter)

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{self.curve['feature']}_marginal_roi.png")
            plt.savefig(
                output_path,
                dpi=300,
                bbox_inches="tight",
                transparent=True,
                facecolor="none",
                edgecolor="none"
            )
            return output_path