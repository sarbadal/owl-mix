import os
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from .base import BasePlotter


@dataclass
class BoxPlotParams:
    n_plot_per_row: int = 4


class BoxPlotter(BasePlotter):

    def __init__(self, data: Dict[str, Dict[str, Any]], params: BoxPlotParams = BoxPlotParams):
        super().__init__(data, params)

    def generate(self, output_dir: str = "outputs/charts") -> Optional[str]:
        n = len(self.data)
        if n == 0:
            print("No data for box plot.")
            return None
        n_cols = min(self.params.n_plot_per_row, n)
        n_rows = math.ceil(n / n_cols)
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(3 * n_cols, 4 * n_rows), constrained_layout=True)
        axes = axes.flatten() if n > 1 else [axes]

        for idx, stats in enumerate(self.data):
            box = {
                'med': stats['median'],
                'q1': stats['Q1'],
                'q3': stats['Q3'],
                'whislo': stats['min'],
                'whishi': stats['max'],
                'fliers': stats.get('outliers', []),
            }
            axes[idx].bxp([box], showfliers=True, widths=0.2)
            axes[idx].set_title(stats['column'])
            axes[idx].set_xticks([])

            outliers = stats.get('outliers', [])
            if outliers:
                x_vals = 1 + np.random.uniform(-0.07, 0.07, size=len(outliers))
                axes[idx].scatter(x_vals, outliers, color='red', s=15, zorder=3)

        # Remove unused axes
        for j in range(idx + 1, len(axes)):
            fig.delaxes(axes[j])

        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, "box_plot_grid.png")

        plt.tight_layout()
        plt.savefig(file_path, dpi=150)
        plt.close()
        
        return file_path

    