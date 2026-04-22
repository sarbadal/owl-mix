# src/owlmix/eda/charts/correlation.py
 
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

from owlmix.eda.utils import ColumnMixin
 
 
class CorrelationChart(ColumnMixin):
    def __init__(self, df, columns: list[str]=None, output_dir: str="charts", precision: int=2):
        self.df = df.copy()
        self.columns = self._get_columns(columns)
        self.output_dir = output_dir
        self.precision = precision

        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self):
        cols = self.columns
        if len(cols) < 2:
            raise ValueError("Need at least 2 columns for correlation")

        corr = self.df[cols].corr()
        num_cols = len(corr.columns)

        # Dynamic figure sizing based on number of columns
        fig_size = max(6, num_cols * 0.8)

        plt.figure(figsize=(fig_size, fig_size))

        # Heatmap using matplotlib (no seaborn)
        im = plt.imshow(corr, interpolation='nearest')

        plt.colorbar(im)

        # Axis ticks
        plt.xticks(
            ticks=np.arange(num_cols),
            labels=corr.columns,
            rotation=45,
            ha="right",
            fontsize=8  # smaller font to avoid overlap
        )

        plt.yticks(
            ticks=np.arange(num_cols),
            labels=corr.columns,
            fontsize=8
        )

        # Annotate values with limited precision
        for i in range(num_cols):
            for j in range(num_cols):
                value = corr.iloc[i, j]
                plt.text(
                    j,
                    i,
                    f"{value:.{self.precision}f}",
                    ha="center",
                    va="center",
                    fontsize=7,
                    color="black"
                )

        plt.title("Correlation Matrix", fontsize=12)

        # Prevent truncation
        plt.tight_layout()

        file_path = os.path.join(self.output_dir, "correlation_matrix.png")
        plt.savefig(file_path, dpi=150)
        plt.close()

        return file_path