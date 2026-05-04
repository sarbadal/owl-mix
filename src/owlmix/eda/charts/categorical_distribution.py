# owlmix/eda/charts/categorical_distribution.py
import os
import math
import logging
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


logger = logging.getLogger(__name__)


class CategoricalDistributionChart:
    def __init__(self, data: dict[str, str|list], output_dir: str = "charts"):
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

    def _generate(self):
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
                    va="center",
                    ha="left",
                    fontsize=7,
                )

            ax.set_title(f"Distribution of {column_name}")
            ax.tick_params(axis='x', labelbottom=False)
            ax.tick_params(axis='y', labelsize=8)

        plt.tight_layout()
        file_path = os.path.join(self.output_dir, "categorical_distribution.png")
        plt.savefig(file_path, dpi=150)
        plt.close()
        return file_path

    def generate(self) -> str:
        """Generates categorical distribution charts for specified columns 
        and saves to file."""
        try:
            return self._generate()
        except Exception as e:
            logger.error({
                "type": "categorical_distribution_chart",
                "error": str(e),
                "status": "failed"
            })
            raise
