import os
import pandas as pd
import matplotlib.pyplot as plt

from typing import TypedDict, NotRequired, Any

from owlmix.eda.utils import ColumnMixin
from owlmix.typing.types import ComparisonType, PlotModeType
from owlmix.typing.normalize import normalize_comparison_type, normalize_plot_mode


class ChartData(TypedDict):
    columns: NotRequired[list[str]]
    data: list[dict[str, Any]]


class ComparisonChart:
    def __init__(
            self,
            data: ChartData,
            comparison_type: ComparisonType = "yoy",
            mode: PlotModeType = "pct_change",
            output_dir: str = "outputs"
    ) -> None:
        """
        mode:
            - 'absolute'     → only actual values
            - 'pct_change'   → only % change
            - 'dual'         → both (dual axis)
        """
        self.mode = normalize_plot_mode(mode)
        self.output_dir = output_dir
        self.df = self._to_dataframe(data)
        self.comparison = normalize_comparison_type(comparison_type)

        # For internal requirement
        self.x_col = "year"
        self.abs_cols, self.pct_cols = self._split_columns()
        self.scale_factor, self.scale_label = self._get_scale()

    def _to_dataframe(self, data: list[dict]) -> pd.DataFrame:
        """Generate a dataframe from the data"""
        return pd.DataFrame(data["data"])

    def _split_columns(self) -> tuple[list[str], list[str]]:
        abs_cols, pct_cols = [], []

        for col in self.df.columns:
            if col == self.x_col:
                continue
            elif col.endswith("_pct_change"):
                pct_cols.append(col)
            else:
                abs_cols.append(col)

        return abs_cols, pct_cols

    def _get_scale(self) -> tuple[int, str]:
        """Auto-scaling (only for absolute)"""
        if not self.abs_cols:
            return 1, ""

        max_val = self.df[self.abs_cols].max().max()

        if max_val >= 1_000_000:
            return 1_000_000, " (in millions)"
        if max_val >= 1_000:
            return 1_000, " (in thousands)"
        return 1, ""

    def _limit_xticks(self, x, max_xticks):
        n = len(x)
        if n <= max_xticks:
            return range(n), x

        step = max(1, n // max_xticks)
        indices = list(range(0, n, step))
        labels = [x[i] for i in indices]

        return indices, labels

    def _compute_max_xticks(self, fig_width_inches: int = 12):
        dpi = 150
        width_px = fig_width_inches * dpi
        return max(4, int(width_px) // 90)

    def _get_xlabel(self, comparison_type: str) -> str:
        comparison_types_dict = {
            "wow": "Week-Over-Week - Week Start Date: YYYY-MM-DD",
            "mom": "Month-Over-Month - YYYY-MM",
            "qoq": "Quarter-Over-Quarter - YYYYQX",
            "yoy": "Year-Over-Year",
            "yoy_month": "Month-Over-Month - YYYY-MM",
            "yoy_quarter": "Quarter-Over-Quarter - YYYYQX",
            "yoy_week": "Week-Over-Week - Week Start Date: YYYY-MM-DD",
        }
        return comparison_types_dict[comparison_type]

    def generate(self) -> str:
        os.makedirs(self.output_dir, exist_ok=True)

        file_path = os.path.join(
            self.output_dir,
            f"{self.comparison}_comparison.png"
        )

        df = self.df.copy()
        df = df.sort_values(by=[self.x_col], ascending=True)

        x = df[self.x_col].astype(str).tolist()
        fig_width, fig_height = 12, 6

        fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))
        max_xticks = self._compute_max_xticks(fig_width)

        # Limit x-axis ticks
        indices, labels = self._limit_xticks(x, max_xticks)

        # ABSOLUTE VALUES
        if self.mode in ["absolute", "dual"]:
            for col in self.abs_cols:
                y = (df[col] / self.scale_factor).round(2)
                ax1.plot(x, y, marker="o", label=col)

            ax1.set_ylabel(f"Values{self.scale_label}")
            ax1.grid(True)

        # PERCENTAGE CHANGE
        if self.mode in ["pct_change", "dual"]:
            ax2 = ax1.twinx() if self.mode == "dual" else ax1

            for col in self.pct_cols:
                y = df[col]
                ax2.plot(x, y, linestyle="--", marker="x", label=col)

            ax2.set_ylabel("% Change")
            ax2.axhline(y=0, linestyle="-", color="grey", linewidth=0.8)

        # X-axis
        xlabel = self._get_xlabel(self.comparison)
        ax1.set_xticks(indices)
        ax1.set_xticklabels(labels, rotation=45)

        ax1.set_title(f"{self.comparison.upper()} Comparison (%)")
        ax1.set_xlabel(xlabel)

        # Legend (merge both axes)
        lines, labels = ax1.get_legend_handles_labels()

        if self.mode == "dual":
            lines2, labels2 = ax2.get_legend_handles_labels()
            lines += lines2
            labels += labels2

        ax1.legend(lines, labels)

        plt.tight_layout()
        plt.savefig(file_path, dpi=150)
        plt.close()

        return file_path
