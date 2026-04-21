# owlmix/eda/charts/categorical_distribution.py
import os
import math
import matplotlib.pyplot as plt
 
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

    def generate(self):
        n = len(self.data)
        n_cols = 2
        n_rows = math.ceil(n / n_cols)
 
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 8))
 
        # Normalize axes
        if n_rows == 1:
            axes = [axes] if n == 1 else axes
        axes = axes.flatten()
 
        for i, item in enumerate(self.data):
            ax = axes[i]
 
            column_name = item["column"]
            categories = item["x"]
            values = item["y"]
 
            ax.barh(categories, values)
 
            ax.set_title(f"Distribution of {column_name}")
 
            # Clean look (optional)
            ax.tick_params(axis='x', labelbottom=False)
            ax.tick_params(axis='y', labelsize=8)
 
        # Hide unused plots
        for j in range(i + 1, len(axes)):
            axes[j].axis("off")
 
        plt.tight_layout()

        file_path = os.path.join(self.output_dir, "categorical_distribution.png")
        plt.savefig(file_path, dpi=150)
        plt.close()
 
        return file_path
 