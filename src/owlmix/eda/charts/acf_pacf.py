# owlmix/eda/charts/acf_pacf.py
import os
import math
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np


class ACFPACFPlotter:
    def __init__(self, data: dict[str, list], output_dir: str="charts"):
        """
        data_dict = {
            "data": [
                {
                    "column": str,
                    "lag": list[int],
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
        if n == 0:
            print("No data provided")
            return None

        fontsize = 14 if n == 1 else None
        labelsize = 12 if n == 1 else None

        cols = min(n, 3)
        rows = math.ceil(n / cols)

        fig, axes = plt.subplots(rows, cols, figsize=(18, 5 * rows))
        axes = np.array(axes).reshape(rows, cols)

        for i, item in enumerate(self.data):
            r, c = divmod(i, cols)
            ax = axes[r][c]

            lags = item["lags"]
            acf_vals = item["acf"]
            pacf_vals = item["pacf"]

            x = np.arange(len(lags))
            width = 0.4

            # Bars
            # ax.bar(x - width / 2, acf_vals, width=width, label="ACF")
            # ax.bar(x + width / 2, pacf_vals, width=width, label="PACF")

            # Bars
            ax.bar(x - width / 2, acf_vals, width=width, label="ACF", alpha=0.8)
            ax.bar(x + width / 2, pacf_vals, width=width, label="PACF", alpha=0.8)

            x_smooth = np.linspace(x.min(), x.max(), 300)

            # ACF smooth
            acf_spline = make_interp_spline(x, acf_vals, k=3)
            acf_smooth = acf_spline(x_smooth)

            # PACF smooth
            pacf_spline = make_interp_spline(x, pacf_vals, k=3)
            pacf_smooth = pacf_spline(x_smooth)

            # Plot smooth lines
            # ax.plot(x_smooth, acf_smooth, linewidth=2)
            # ax.plot(x_smooth, pacf_smooth, linewidth=2)

            # ACF → Thick smooth line (background)
            ax.plot(
                x_smooth if 'x_smooth' in locals() else x,
                acf_smooth if 'acf_smooth' in locals() else acf_vals,
                linewidth=5,
                linestyle='solid',
                alpha=0.2,
                label='ACF (smooth)',
                zorder=2
            )

            # PACF → Thin dotted line (foreground)
            ax.plot(
                x_smooth if 'x_smooth' in locals() else x,
                pacf_smooth if 'pacf_smooth' in locals() else pacf_vals,
                linewidth=2,
                linestyle='dotted',
                alpha=0.2,
                label='PACF (dotted)',
                zorder=3
            )
            # end of bar

            # Increase axis tick label size
            ax.tick_params(axis='both', labelsize=labelsize)

            # Increase title size
            ax.set_title(f"{item['column']}", fontsize=fontsize)

            # Increase axis label sizes (if you have them)
            ax.set_xlabel("Lags", fontsize=fontsize)
            ax.set_ylabel("Value", fontsize=fontsize)

            # Increase legend font size
            ax.legend(fontsize=fontsize)

            # Formatting
            ax.set_title(f"{item['column']}", fontsize=fontsize)
            ax.set_xticks(x)
            ax.set_xticklabels(lags)
            ax.tick_params(axis='both', labelsize=labelsize)
            ax.axhline(0)  # baseline

            threshold = 1.96 / np.sqrt(len(lags))
            ax.axhline(threshold, linestyle="--", linewidth=1)
            ax.axhline(-threshold, linestyle="--", linewidth=1)

            ax.legend()

        # Hide empty plots
        total_plots = rows * cols
        for j in range(n, total_plots):
            r, c = divmod(j, cols)
            axes[r][c].axis("off")

        plt.tight_layout()

        file_path = os.path.join(self.output_dir, "acf_pacf.png")
        plt.savefig(file_path, dpi=150)
        plt.close()

        return file_path