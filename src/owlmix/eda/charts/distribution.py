import os
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm

from owlmix.eda.utils import ColumnMixin


class DistributionChart(ColumnMixin):
    def __init__(self, df: pd.DataFrame, columns: list[str] = None, output_dir: str="charts"):
        self.df = df.copy()
        self.columns = self._get_columns(columns)
        self.output_dir = output_dir

    def generate(self, max_charts_per_row: int = 3) -> str:
        n = len(self.columns)

        # Grid calculation (auto layout)
        cols = min(max_charts_per_row, n)
        rows = math.ceil(n / cols)

        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))

        # Normalize axes shape
        if n == 1:
            axes = [[axes]]
        elif rows == 1:
            axes = [axes]

        axes = np.array(axes).reshape(rows, cols)

        for idx, col in enumerate(self.columns):
            r, c = divmod(idx, cols)
            ax = axes[r][c]

            data = self.df[col].dropna()

            if len(data) == 0:
                ax.set_title(f"{col} (no data)")
                continue

            # Histogram
            ax.hist(data, bins=30, density=True, alpha=0.6)

            # Fit normal distribution
            mu, std = norm.fit(data)

            # Smooth curve
            x_min, x_max = ax.get_xlim()
            x = np.linspace(x_min, x_max, 100)
            p = norm.pdf(x, mu, std)

            ax.plot(x, p)
            ax.set_title(col)

        # Remove empty subplots
        for idx in range(n, rows * cols):
            r, c = divmod(idx, cols)
            fig.delaxes(axes[r][c])

        plt.tight_layout()

        file_path = os.path.join(self.output_dir, "distribution_grid.png")
        plt.savefig(file_path, dpi=150)
        plt.close()

        return file_path
