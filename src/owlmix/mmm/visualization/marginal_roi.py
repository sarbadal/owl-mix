import os
import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from typing import Dict, Tuple


@dataclass
class MarginalROIPlotConfig:
    line_color: str = "#1f77b4"  # blue
    fitted_line_color: str = "#ff7f0e"  # orange
    label_color: str = "#888888"  # neutral gray
    font_size: int = 16


def _trim_num(s: str) -> str:
    return s.rstrip("0").rstrip(".")

def _fmt_pct(v: float, digits: int) -> str:
    return f"{_trim_num(f'{v*100:.{digits}f}')}%"

def y_formatter(v: float, _) -> str:
    if v == 0:
        return "0"
    if abs(v) >= 1_000:
        return _trim_num(f"{v/1_000:.1f}") + "K"
    if abs(v) >= 1:
        return _trim_num(f"{v:.2f}")
    if abs(v) >= 0.1:
        return _fmt_pct(v, 3)
    if abs(v) >= 0.01:
        return _fmt_pct(v, 4)
    if abs(v) >= 0.001:        
        return _fmt_pct(v, 5)
    if abs(v) >= 0.0001:
        return _fmt_pct(v, 6)
    return _fmt_pct(v, 7)


class MarginalROIPlotter:
    """Plots marginal ROI curve with optional fitted curve and saves the chart as a PNG file."""
    def __init__(self, curve: Dict, classification: Dict, params: MarginalROIPlotConfig | None = None):
        self.curve = curve
        self.classification = classification
        self.params = params or MarginalROIPlotConfig()
        self.min_threshold = classification["thresholds"]["low"]
        self.max_threshold = classification["thresholds"]["high"]

    def plot(self, output_dir: str = "outputs/charts") -> str:
        x = self.curve["input_value"]
        y = self.classification["marginal"]

        fig, ax = plt.subplots()
        x_arr, y_arr = self._prepare_arrays(x, y)
        y_low, y_high, x_low, x_high = self._threshold_points(x_arr, y_arr)

        self._draw_main_curve(ax, x, y)
        self._draw_threshold_guides(ax, y_low, y_high, x_low, x_high)
        self._draw_threshold_points(ax, x_low, x_high, y_low, y_high)
        self._annotate_optimal_spend(ax, x_low, x_high)
        self._style_axes(ax)

        fig.tight_layout()
        return self._save_figure(fig, output_dir)

    def _prepare_arrays(self, x, y) -> Tuple[np.ndarray, np.ndarray]:
        return np.asarray(x, dtype=float), np.asarray(y, dtype=float)

    def _threshold_points(self, x_arr: np.ndarray, y_arr: np.ndarray) -> Tuple[float, float, float, float]:
        y_low = float(self.min_threshold)
        y_high = float(self.max_threshold)
        x_low = float(x_arr[np.argmin(np.abs(y_arr - y_low))])
        x_high = float(x_arr[np.argmin(np.abs(y_arr - y_high))])
        return y_low, y_high, x_low, x_high

    def _draw_main_curve(self, ax, x, y) -> None:
        ax.plot(
            x,
            y,
            label="Marginal ROI",
            color=self.params.line_color,
            alpha=0.95,
            linewidth=3,
        )

    def _draw_threshold_guides(self, ax: plt.Axes, y_low: float, y_high: float, x_low: float, x_high: float) -> None:
        ax.hlines(
            [y_low, y_high],
            xmin=[0, 0],
            xmax=[x_low, x_high],
            colors=self.params.label_color,
            linestyles="--",
            linewidth=1.5,
            alpha=0.2,
        )
        ax.vlines(
            [x_low, x_high],
            ymin=[min(y_low, 0), min(y_high, 0)],
            ymax=[max(y_low, 0), max(y_high, 0)],
            colors=self.params.label_color,
            linestyles="-",
            linewidth=1.5,
            alpha=0.9,
        )

    def _draw_threshold_points(self, ax: plt.Axes, x_low: float, x_high: float, y_low: float, y_high: float) -> None:
        ax.scatter(
            [x_low, x_high],
            [y_low, y_high],
            color=self.params.label_color,
            s=40,
            zorder=5
        )

    def _annotate_optimal_spend(self, ax: plt.Axes, x_low: float, x_high: float) -> None:
        x_left, x_right = sorted([x_low, x_high])
        y_min_lim, y_max_lim = ax.get_ylim()
        y_range = y_max_lim - y_min_lim
        y_arrow = y_min_lim + 0.05 * y_range
        y_text = y_arrow + 0.02 * y_range

        ax.annotate(
            "",
            xy=(x_left, y_arrow),
            xytext=(x_right, y_arrow),
            arrowprops=dict(arrowstyle="<->", color=self.params.label_color, lw=2),
            annotation_clip=False,
        )
        ax.text(
            (x_left + x_right) / 2,
            y_text,
            "Optimal Spend",
            ha="center",
            va="bottom",
            rotation=90,
            color=self.params.label_color,
            fontsize=max(self.params.font_size - 4, 9),
        )

    def _style_axes(self, ax: plt.Axes) -> None:
        label_color = self.params.label_color
        ax.set_xlabel(self.curve["feature"], color=label_color, fontsize=self.params.font_size)
        ax.set_ylabel("Marginal ROI", color=label_color, fontsize=self.params.font_size)
        ax.legend(fontsize=self.params.font_size)

        ax.tick_params(colors=label_color, labelsize=self.params.font_size)
        for spine in ax.spines.values():
            spine.set_color(label_color)

        ax.xaxis.set_major_formatter(
            FuncFormatter(lambda x, _: f"{int(x / 1000)}K" if abs(x) >= 1000 else f"{int(x)}")
        )
        ax.yaxis.set_major_formatter(FuncFormatter(y_formatter))

    def _save_figure(self, fig: plt.Figure, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{self.curve['feature']}_marginal_roi.png")
        fig.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight",
            transparent=True,
            facecolor="none",
            edgecolor="none",
        )
        return output_path