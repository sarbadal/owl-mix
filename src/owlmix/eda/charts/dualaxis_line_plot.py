# owlmix/eda/charts/dualaxis_line_plot.py
import matplotlib.pyplot as plt
import os

MAX_X_TICKS = 15


class DualAxisLinePlotter:
    def __init__(self, data: dict[str, list], output_dir: str="charts"):
        """
        data: dict = {
            "data": [
                {
                    "column": str,
                    "x": list[int],
                    "target": [...],
                    "feature": [...]
                }
                ...
            ]
        }
        """
        self.data = data
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

    def _get_tick_positions(self, x):
        """Return indices to show as ticks"""
        n = len(x)
        max_x_ticks = MAX_X_TICKS

        if n <= max_x_ticks:
            return list(range(n))

        step = max(1, n // max_x_ticks)
        return list(range(0, n, step))

    def generate(self):
        n = len(self.data)

        if n == 0:
            raise ValueError("No data provided")

        fig, axes = plt.subplots(n, 1, figsize=(12, 5 * n))

        # If only one plot, axes is not a list
        if n == 1:
            axes = [axes]

        for ax, item in zip(axes, self.data):
            kpi = item["kpi"]
            column = item["column"]
            x = item.get("x", [])
            y1 = item.get("target", [])
            y2 = item.get("feature", [])
            title = item.get("column", "Unknown")

            if not (len(x) == len(y1) == len(y2)):
                raise ValueError(f"Length mismatch in column: {title}")

            # Primary axis (target)
            ax.plot(x, y1, marker='o', color='tab:blue', linewidth=2)
            ax.set_ylabel(f"Target - {kpi}")
            ax.set_title(title)

            # Secondary axis (feature)
            ax2 = ax.twinx()
            ax2.plot(x, y2, linestyle='--', marker='x', color='tab:orange', linewidth=1.5)
            ax2.set_ylabel(f"Feature column - {column}")

            # Rotate X labels if dates
            # 👇 Smart tick selection
            tick_idx = self._get_tick_positions(x)
            ax.set_xticks(tick_idx)
            ax.set_xticklabels([x[i] for i in tick_idx], rotation=45)
            # ax.tick_params(axis='x', rotation=45)

        plt.tight_layout()

        file_path = os.path.join(self.output_dir, "kpi_vs_feature.png")
        plt.savefig(file_path, dpi=150, bbox_inches="tight")
        plt.close()

        return file_path
