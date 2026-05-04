# owlmix/eda/charts/dualaxis_line_plot.py
import matplotlib.pyplot as plt
import os
import logging


logger = logging.getLogger(__name__)


class DualAxisLinePlotter:
    MAX_X_TICKS = 18

    def __init__(self, data: list[dict], output_dir: str = "charts"):
        """
        data: list of dicts, each dict should have:
            {
                "kpi": str,
                "column": str,
                "x": list,
                "target": list,
                "feature": list
            }
        """
        self.data = data
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _get_tick_positions(self, x):
        """Return indices to show as ticks"""
        n = len(x)
        if n <= self.MAX_X_TICKS:
            return list(range(n))
        step = max(1, n // self.MAX_X_TICKS)
        return list(range(0, n, step))

    def _generate(self):
        n = len(self.data)
        if n == 0:
            raise ValueError("No data provided")

        fig, axes = plt.subplots(n, 1, figsize=(12, 5 * n))
        if n == 1:
            axes = [axes]

        for ax, item in zip(axes, self.data):
            kpi = item.get("kpi", "Unknown KPI")
            column = item.get("column", "Unknown Column")
            x = item.get("x", [])
            y1 = item.get("target", [])
            y2 = item.get("feature", [])
            title = column

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

            # Smart tick selection
            tick_idx = self._get_tick_positions(x)
            ax.set_xticks(tick_idx)
            ax.set_xticklabels([x[i] for i in tick_idx], rotation=45)

        plt.tight_layout()
        file_path = os.path.join(self.output_dir, "kpi_vs_feature.png")
        plt.savefig(file_path, dpi=150, bbox_inches="tight")
        plt.close()
        return file_path

    def generate(self):
        try:
            return self._generate()
        except Exception as e:
            logger.error({
                "type": "dualaxis_line_plot", 
                "error": str(e), 
                "status": "failed"
            })
            raise
