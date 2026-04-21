# owlmix/eda/charts/categorical_distribution.py
import os
import math
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

 
class CategoricalDistributionChart:
    def __init__(self, data: dict[str, str|list], output_dir: str="charts"):
        """
        data: list of dicts
        Each dict must have:
            - column: str
            - x: list of categories
            - y: list of counts
        """
        self.data = data
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, output_path="categorical_distribution.png"):
        n = len(self.data)
        n_cols = 2
        n_rows = math.ceil(n / n_cols)

        fig = plt.figure(figsize=(14, 8))
        gs = GridSpec(n_rows, n_cols, figure=fig)

        axes = []

        for i, item in enumerate(self.data):
            row = i // 2
            col = i % 2

            # If last chart and odd → span full row
            if i == n - 1 and n % 2 != 0:
                ax = fig.add_subplot(gs[row, :])  # span both columns
            else:
                ax = fig.add_subplot(gs[row, col])

            axes.append(ax)

            column_name = item["column"]
            categories = item["x"]
            values = item["y"]

            # Plot
            ax.barh(categories, values)

            for index, value in enumerate(values):
                ax.text(
                    value,
                    index,
                    f"{value}",
                    va="center",  # 'top', 'bottom', 'center', 'baseline', 'center_baseline'
                    ha="left",  # 'center', 'right', 'left'
                    fontsize=7,
                )

            ax.set_title(f"Distribution of {column_name}")

            # Clean look (optional)
            ax.tick_params(axis='x', labelbottom=False)
            ax.tick_params(axis='y', labelsize=8)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150)
        plt.close()

        return output_path
 