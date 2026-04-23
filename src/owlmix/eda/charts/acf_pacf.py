# owlmix/eda/charts/acf_pacf.py
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from scipy.interpolate import make_interp_spline


def get_colors(values) -> list:
    norm = mcolors.Normalize(vmin=-1, vmax=1)  # ACF/PACF range
    cmap = cm.get_cmap("coolwarm")  # blue ↔ red
    return [cmap(norm(v)) for v in values]


class ACFPACFPlotter:
    def __init__(self, data: dict[str, list], output_dir: str="charts"):
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

        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self) -> str:
        n = len(self.data)

        # Create grid: one row per column, 2 charts (ACF, PACF)
        fig, axes = plt.subplots(nrows=n, ncols=2, figsize=(14, 4 * n))

        # Handle single row case
        if n == 1:
            axes = np.array([axes])

        for i, item in enumerate(self.data):
            col_name = item["column"]
            lags = item["lags"]
            acf_vals = item["acf"]
            pacf_vals = item["pacf"]
            n_obs = item["n_obs"]

            conf = 1.96 / np.sqrt(n_obs)

            # -------------------
            # ACF Plot
            # -------------------
            ax_acf = axes[i, 0]
            markerline, stemlines, baseline = ax_acf.stem(lags, acf_vals, basefmt=" ")
            markerline.set_markersize(6)
            markerline.set_color("red")
            stemlines.set_linewidth(2.5)
            stemlines.set_color("red")

            # Confidence band
            ax_acf.axhspan(-conf, conf, alpha=0.15, color="blue")

            # Integer ticks
            ax_acf.set_xticks(lags)
            ax_acf.set_xlim(min(lags) - 0.5, max(lags) + 0.5)

            ax_acf.set_title(
                f"ACF - {col_name} (N={n_obs})",
                fontsize=14,
                fontweight="bold",
            )
            ax_acf.set_xlabel("Lags", fontsize=14)
            ax_acf.set_ylabel("ACF", fontsize=14)

            ax_acf.hlines(
                y=acf_vals,
                xmin=[lag - 0.5 for lag in lags],
                xmax=[lag + 0.5 for lag in lags],
                colors='gray',
                linestyles='solid',
                linewidth=2,
                alpha=0
            )

            # -------------------
            # PACF Plot
            # -------------------
            ax_pacf = axes[i, 1]
            markerline, stemlines, baseline = ax_pacf.stem(lags, pacf_vals, basefmt=" ")
            markerline.set_markersize(6)
            stemlines.set_linewidth(2.5)

            # Confidence band
            ax_pacf.axhspan(-conf, conf, alpha=0.15, color="gray")

            # Integer ticks
            ax_pacf.set_xticks(lags)
            ax_pacf.set_xlim(min(lags) - 0.5, max(lags) + 0.5)

            ax_pacf.set_title(
                f"PACF - {col_name} (N={n_obs})",
                fontsize=14,
                fontweight="bold",
            )
            ax_pacf.set_xlabel("Lags", fontsize=14)
            ax_pacf.set_ylabel("PACF", fontsize=14)

            ax_pacf.hlines(
                y=acf_vals,
                xmin=[lag - 0.5 for lag in lags],
                xmax=[lag + 0.5 for lag in lags],
                colors='gray',
                linestyles='solid',
                linewidth=2,
                alpha=0
            )

        plt.tight_layout()

        file_path = os.path.join(self.output_dir, "acf_pacf.png")
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()

        return file_path
