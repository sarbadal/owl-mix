import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from dataclasses import dataclass
from scipy.interpolate import make_interp_spline
from typing import Dict, Any, List

from .base import BasePlotter

@dataclass
class AcfPacfPlotParams:
    """
    Configuration for ACF/PACF plot colors.

    Attributes:
        acf_marker (str): Color for ACF markers.
        pacf_marker (str): Color for PACF markers.
        acf_stem (str): Color for ACF stem lines.
        pacf_stem (str): Color for PACF stem lines.
        acf_conf (str): Color for ACF confidence interval.
        pacf_conf (str): Color for PACF confidence interval.
    """
    acf_marker: str = "red"
    pacf_marker: str = "steelblue"
    acf_stem: str = "red"
    pacf_stem: str = "steelblue"
    acf_conf: str = "blue"
    pacf_conf: str = "gray"


class AcfPacfPlotter(BasePlotter):

    def __init__(self, data: Dict[str, Dict[str, Any]], params: AcfPacfPlotParams | None = None):
        super().__init__(data, params or AcfPacfPlotParams())
        self.y_neg_break = self._get_dynamic_y_neg_break()
        self.y_pos_break = 0.2
        self.y_pos_resume = 0.9
        self.y_max = 1.02

    def _get_dynamic_y_neg_break(self):
        min_acf = min(min(item["acf"]) for item in self.data)
        min_pacf = min(min(item["pacf"]) for item in self.data)
        return min(min_acf, min_pacf, -0.09) - 0.01  # fallback to -0.1 if all values are higher

    def _get_max_positive_lag_value(self, values, lags):
        """Return the maximum value for lags > 0."""
        return max([v for v, lag in zip(values, lags) if lag > 0], default=0)

    def _get_min_positive_lag_value(self, values, lags):
        """Return the minimum value for lags > 0."""
        return min([v for v, lag in zip(values, lags) if lag > 0], default=0)

    def generate(self, output_dir: str = "outputs/charts") -> str:
        """Combines all plots into one large vertical image."""
        n = len(self.data)
        fig, axes = plt.subplots(
            nrows=2 * n, ncols=2, figsize=(14, 7 * n),
            gridspec_kw={'height_ratios': [1, 2] * n}
        )
        if n == 1: axes = np.array(axes).reshape(2, 2)

        for i, item in enumerate(self.data):
            self._plot_metric_pair(item, axes[2*i : 2*i+2, :])

        return self._save_and_close(fig, os.path.join(output_dir, "acf_pacf.png"))

    def generate_chart_for_all(self, output_dir: str = "outputs/charts") -> dict:
        """Generates individual image files for each column."""
        os.makedirs(output_dir, exist_ok=True)
        charts = {}

        for item in self.data:
            fig, axes = plt.subplots(
                nrows=2, ncols=2, figsize=(20, 7),
                gridspec_kw={"height_ratios": [1, 4]}
            )
            self._plot_metric_pair(item, axes)
            
            safe_name = "".join(c if c.isalnum() else "_" for c in str(item["column"]))
            path = os.path.join(output_dir, f"acf_pacf_{safe_name}.png")
            charts[item["column"]] = self._save_and_close(fig, path)
            
        return charts

    def _plot_metric_pair(self, item, axes_subset):
        """Core logic: Plots ACF (left col) and PACF (right col) across 2 rows."""
        conf = 1.96 / np.sqrt(item["n_obs"])
        
        # Left Column: ACF | Right Column: PACF
        for col_idx, mode in enumerate(["acf", "pacf"]):
            top_ax = axes_subset[0, col_idx]
            btm_ax = axes_subset[1, col_idx]
            
            self._draw_broken_axis(top_ax, btm_ax, item, mode, conf)

    def _draw_broken_axis(self, top, btm, item, mode, conf):
        """Handles the actual stem plotting and styling for one metric."""
        vals = item[mode]
        lags = item["lags"]
        params = self.params
        
        # Get mode-specific styles
        stem_fmt = getattr(params, f"{mode}_stem")
        marker_fmt = getattr(params, f"{mode}_marker")
        color_conf = getattr(params, f"{mode}_conf", "blue") # fallback

        for ax in [top, btm]:
            ax.stem(lags, vals, basefmt=" ", linefmt=stem_fmt, markerfmt=marker_fmt)
            ax.axhspan(-conf, conf, alpha=0.15, color=color_conf)
            ax.set_xticks(lags)
            ax.set_xlim(min(lags) - 0.5, max(lags) + 0.5)
            ax.tick_params(axis="both", labelsize=18)

        # Styling Top
        top.set_ylim(self.y_pos_resume, self.y_max)
        top.spines["bottom"].set_visible(False)
        top.tick_params(labelbottom=False)
        top.set_title(f"{mode.upper()} - {item['column']} (N={item['n_obs']})", fontsize=22)

        # Styling Bottom
        v_min = self._get_min_positive_lag_value(vals, lags)
        v_max = self._get_max_positive_lag_value(vals, lags)
        btm.set_ylim(min(self.y_neg_break, v_min), max(self.y_pos_break, v_max))
        btm.spines["top"].set_visible(False)
        btm.set_ylabel(mode.upper())

        self._apply_break_marks(top, btm)

    def _apply_break_marks(self, top, btm):
        d = 0.015
        for ax, y_pos in [(top, 0), (btm, 1)]:
            kwargs = dict(transform=ax.transAxes, color="k", clip_on=False)
            ax.plot((-d, +d), (y_pos - d, y_pos + d), **kwargs)
            ax.plot((1 - d, 1 + d), (y_pos - d, y_pos + d), **kwargs)

    def _save_and_close(self, fig, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        fig.tight_layout()
        fig.savefig(path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        return path
