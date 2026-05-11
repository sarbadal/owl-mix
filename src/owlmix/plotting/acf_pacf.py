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

    def __init__(self, data: Dict[str, Dict[str, Any]], params: AcfPacfPlotParams = AcfPacfPlotParams):
        super().__init__(data, params)
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
        n = len(self.data)
        fig_height = 7 * n

        fig, axes = plt.subplots(
            nrows=2 * n, ncols=2, figsize=(14, fig_height),
            gridspec_kw={'height_ratios': [1, 2] * n}
        )
        if n == 1:
            axes = np.array(axes).reshape(2, 2)

        for i, item in enumerate(self.data):
            col_name = item["column"]
            lags = item["lags"]
            acf_vals = item["acf"]
            pacf_vals = item["pacf"]
            n_obs = item["n_obs"]

            acf_max_pos = self._get_max_positive_lag_value(acf_vals, lags)
            acf_min_pos = self._get_min_positive_lag_value(acf_vals, lags)

            conf = 1.96 / np.sqrt(n_obs)

            acf_max_pos = self._get_max_positive_lag_value(acf_vals, lags)
            acf_min_pos = self._get_min_positive_lag_value(acf_vals, lags)
            pacf_max_pos = self._get_max_positive_lag_value(pacf_vals, lags)
            pacf_min_pos = self._get_min_positive_lag_value(pacf_vals, lags)

            # --- ACF broken axis ---
            ax_acf_top = axes[2 * i, 0]
            ax_acf_bottom = axes[2 * i + 1, 0]
            

            # Top (shows only high values)
            ax_acf_top.stem(lags, acf_vals, basefmt=" ", linefmt=self.params.acf_stem, markerfmt=self.params.acf_marker)
            ax_acf_top.axhspan(-conf, conf, alpha=0.15, color=self.params.acf_conf)
            ax_acf_top.set_ylim(self.y_pos_resume, self.y_max)
            ax_acf_top.set_yticks(np.arange(self.y_pos_resume, self.y_max + 0.01, 0.1))
            ax_acf_top.spines['bottom'].set_visible(False)
            ax_acf_top.tick_params(labelbottom=False)
            ax_acf_top.set_title(f"ACF - {col_name} (N={n_obs})", fontsize=14, fontweight="bold")

            # Bottom (zooms in on small values)
            ax_acf_bottom.stem(lags, acf_vals, basefmt=" ", linefmt=self.params.acf_stem, markerfmt=self.params.acf_marker)
            ax_acf_bottom.axhspan(-conf, conf, alpha=0.15, color=self.params.acf_conf)
            # ax_acf_bottom.set_ylim(self.y_neg_break, self.y_pos_break)

            ax_acf_bottom.set_ylim(
                min(self.y_neg_break, acf_min_pos), 
                max(self.y_pos_break, acf_max_pos)
            )

            ax_acf_bottom.set_yticks(np.arange(self.y_neg_break, self.y_pos_break + 0.01, 0.1))
            ax_acf_bottom.spines['top'].set_visible(False)
            ax_acf_bottom.set_xlabel("Lags", fontsize=14)
            ax_acf_bottom.set_ylabel("ACF", fontsize=14)

            # Diagonal lines for break
            d = .015
            kwargs = dict(transform=ax_acf_top.transAxes, color='k', clip_on=False)
            ax_acf_top.plot((-d, +d), (-d, +d), **kwargs)
            ax_acf_top.plot((1 - d, 1 + d), (-d, +d), **kwargs)
            kwargs.update(transform=ax_acf_bottom.transAxes)
            ax_acf_bottom.plot((-d, +d), (1 - d, 1 + d), **kwargs)
            ax_acf_bottom.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

            # --- PACF broken axis ---
            ax_pacf_top = axes[2 * i, 1]
            ax_pacf_bottom = axes[2 * i + 1, 1]
            

            ax_pacf_top.stem(lags, pacf_vals, basefmt=" ", linefmt=self.params.pacf_stem, markerfmt=self.params.pacf_marker)
            ax_pacf_top.axhspan(-conf, conf, alpha=0.15, color=self.params.pacf_conf)
            ax_pacf_top.set_ylim(self.y_pos_resume, self.y_max)
            ax_pacf_top.set_yticks(np.arange(self.y_pos_resume, self.y_max + 0.01, 0.1))
            ax_pacf_top.spines['bottom'].set_visible(False)
            ax_pacf_top.tick_params(labelbottom=False)
            ax_pacf_top.set_title(f"PACF - {col_name} (N={n_obs})", fontsize=14, fontweight="bold")

            ax_pacf_bottom.stem(lags, pacf_vals, basefmt=" ", linefmt=self.params.pacf_stem, markerfmt=self.params.pacf_marker)
            ax_pacf_bottom.axhspan(-conf, conf, alpha=0.15, color=self.params.pacf_conf)

            ax_pacf_bottom.set_ylim(
                min(self.y_neg_break, pacf_min_pos), 
                max(self.y_pos_break, pacf_max_pos)
            )

            ax_pacf_bottom.set_yticks(np.arange(self.y_neg_break, self.y_pos_break + 0.01, 0.1))
            ax_pacf_bottom.spines['top'].set_visible(False)
            ax_pacf_bottom.set_xlabel("Lags", fontsize=14)
            ax_pacf_bottom.set_ylabel("PACF", fontsize=14)

            # Diagonal lines for break
            kwargs = dict(transform=ax_pacf_top.transAxes, color='k', clip_on=False)
            ax_pacf_top.plot((-d, +d), (-d, +d), **kwargs)
            ax_pacf_top.plot((1 - d, 1 + d), (-d, +d), **kwargs)
            kwargs.update(transform=ax_pacf_bottom.transAxes)
            ax_pacf_bottom.plot((-d, +d), (1 - d, 1 + d), **kwargs)
            ax_pacf_bottom.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

            # Set x-ticks for all
            for ax in [ax_acf_top, ax_acf_bottom, ax_pacf_top, ax_pacf_bottom]:
                ax.set_xticks(lags)
                ax.set_xlim(min(lags) - 0.5, max(lags) + 0.5)

        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, "acf_pacf.png")
        
        plt.tight_layout()
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return file_path
