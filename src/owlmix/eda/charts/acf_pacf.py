# owlmix/eda/charts/acf_pacf.py
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from dataclasses import dataclass
from scipy.interpolate import make_interp_spline

@dataclass
class AcfPacfColorConfig:
    acf_marker: str = "red"
    pacf_marker: str = "steelblue"
    acf_stem: str = "red"
    pacf_stem: str = "steelblue"
    acf_conf: str = "blue"
    pacf_conf: str = "gray"


class ACFPACFPlotter:
    def __init__(self, data: dict[str, list], output_dir: str="charts", color_config: AcfPacfColorConfig = None):
        """
        data_dict = {
            "data": [
                {
                    "column": str,
                    "lags": list[int],
                    "acf": list[float],
                    "pacf": list[float]
                }
            ]
        }
        """
        self.data = data
        self.output_dir = output_dir
        self.color_config = color_config or AcfPacfColorConfig()
        self.y_neg_break = -0.12
        self.y_pos_break = 0.2
        self.y_pos_resume = 0.9
        self.y_max = 1.02

        os.makedirs(self.output_dir, exist_ok=True)

    def _get_max_positive_lag_value(self, values, lags):
        """Return the maximum value for lags > 0."""
        return max([v for v, lag in zip(values, lags) if lag > 0], default=0)

    def _get_min_positive_lag_value(self, values, lags):
        """Return the minimum value for lags > 0."""
        return min([v for v, lag in zip(values, lags) if lag > 0], default=0)

    def generate(self) -> str:
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
            ax_acf_top.stem(lags, acf_vals, basefmt=" ", linefmt=self.color_config.acf_stem, markerfmt=self.color_config.acf_marker)
            ax_acf_top.axhspan(-conf, conf, alpha=0.15, color=self.color_config.acf_conf)
            ax_acf_top.set_ylim(self.y_pos_resume, self.y_max)
            ax_acf_top.set_yticks(np.arange(self.y_pos_resume, self.y_max + 0.01, 0.1))
            ax_acf_top.spines['bottom'].set_visible(False)
            ax_acf_top.tick_params(labelbottom=False)
            ax_acf_top.set_title(f"ACF - {col_name} (N={n_obs})", fontsize=14, fontweight="bold")

            # Bottom (zooms in on small values)
            ax_acf_bottom.stem(lags, acf_vals, basefmt=" ", linefmt=self.color_config.acf_stem, markerfmt=self.color_config.acf_marker)
            ax_acf_bottom.axhspan(-conf, conf, alpha=0.15, color=self.color_config.acf_conf)
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
            

            ax_pacf_top.stem(lags, pacf_vals, basefmt=" ", linefmt=self.color_config.pacf_stem, markerfmt=self.color_config.pacf_marker)
            ax_pacf_top.axhspan(-conf, conf, alpha=0.15, color=self.color_config.pacf_conf)
            ax_pacf_top.set_ylim(self.y_pos_resume, self.y_max)
            ax_pacf_top.set_yticks(np.arange(self.y_pos_resume, self.y_max + 0.01, 0.1))
            ax_pacf_top.spines['bottom'].set_visible(False)
            ax_pacf_top.tick_params(labelbottom=False)
            ax_pacf_top.set_title(f"PACF - {col_name} (N={n_obs})", fontsize=14, fontweight="bold")

            ax_pacf_bottom.stem(lags, pacf_vals, basefmt=" ", linefmt=self.color_config.pacf_stem, markerfmt=self.color_config.pacf_marker)
            ax_pacf_bottom.axhspan(-conf, conf, alpha=0.15, color=self.color_config.pacf_conf)
            # ax_pacf_bottom.set_ylim(self.y_neg_break, self.y_pos_break)

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

        plt.tight_layout()
        file_path = os.path.join(self.output_dir, "acf_pacf.png")
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        return file_path

