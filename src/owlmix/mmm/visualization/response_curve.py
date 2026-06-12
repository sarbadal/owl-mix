import os
import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from typing import Any, Dict, Tuple


@dataclass
class ResponsePlotConfig:
    line_color: str = "#1f77b4"  # blue
    fitted_line_color: str = "#ff7f0e"  # orange
    label_color: str = "#888888"  # neutral gray
    font_size: int = 16


class ResponsePlotter:
    """Plots response curve with optional fitted curve and saves the chart as a PNG file."""
    def __init__(self, curve: Dict, current_spend: float, params: ResponsePlotConfig | None = None):
        self.curve = curve
        self.current_spend = current_spend
        self.params = params or ResponsePlotConfig()

    def plot(self, output_dir: str = "outputs/charts") -> str:
        """Main method to plot the response curve."""
        fig, ax = plt.subplots()

        x_current, y_current = self._get_current_spend_point()
        self._plot_main_curve(ax)
        self._draw_current_spend_annotation(ax, x_current, y_current)
        self._style_axes(ax)
        self._finalize_plot(fig, ax)
        return self._save_plot(fig, output_dir)

    def _plot_main_curve(self, ax) -> None:
        """Plots the main response curve."""
        x = self.curve["input_value"]
        y = self.curve["predicted_target"]
        ax.plot(
            x, y, label="Response",
            color=self.params.line_color,
            alpha=0.95,
            linewidth=3  # Increased thickness
        )

    def _style_axes(self, ax) -> None:
        """Applies styling to the axes."""
        label_color = self.params.label_color
        ax.set_xlabel(self.curve["feature"], color=label_color, fontsize=self.params.font_size)
        ax.set_ylabel("Target", color=label_color, fontsize=self.params.font_size)
        ax.legend(fontsize=self.params.font_size)

        ax.tick_params(colors=label_color, labelsize=self.params.font_size)
        for spine in ax.spines.values():
            spine.set_color(label_color)

        formatter = FuncFormatter(lambda x, _: f'{int(x/1000)}K' if abs(x) >= 1000 else f'{int(x)}')
        ax.xaxis.set_major_formatter(formatter)
        ax.yaxis.set_major_formatter(formatter)

    def _get_current_spend_point(self) -> Tuple[float, float]:
        """Calculates the current spend point on the curve."""
        x_arr = np.asarray(self.curve["input_value"], dtype=float)
        y_arr = np.asarray(self.curve["predicted_target"], dtype=float)

        x_current = float(self.current_spend)
        y_current = float(np.interp(x_current, x_arr, y_arr))
        return x_current, y_current

    def _draw_current_spend_annotation(self, ax: plt.Axes, x_current: float, y_current: float) -> None:
        # Freeze limits from the already-plotted curve
        x_lim = ax.get_xlim()
        y_lim = ax.get_ylim()

        y_bottom = y_lim[0]  # visual x-axis (bottom of plot area), not numeric 0

        ax.vlines(
            x_current,
            ymin=min(y_bottom, y_current),
            ymax=max(y_bottom, y_current),
            colors=self.params.line_color,
            linestyles="--",
            linewidth=2,
            alpha=0.9,
        )

        # Circle at the bottom axis position
        ax.scatter(
            [x_current],
            [y_bottom],
            s=90,
            facecolors="none",
            edgecolors=self.params.line_color,
            linewidths=2,
            zorder=6,
            label="Current Spend",
        )

        # Marker on the curve
        ax.scatter(
            [x_current],
            [y_current],
            s=45,
            color=self.params.line_color,
            zorder=7,
        )

        # Restore limits so annotation cannot rescale the chart
        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)

    def _finalize_plot(self, fig, ax) -> None:
        """Finalizes the plot layout."""
        fig.tight_layout()

    def _save_plot(self, fig, output_dir: str) -> str:
        """Saves the plot to the specified directory."""
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            save_path = os.path.join(output_dir, f"{self.curve['feature']}_response.png")
            fig.savefig(
                save_path,
                dpi=300,
                bbox_inches="tight",
                transparent=True,
                facecolor="none",
                edgecolor="none"
            )
            plt.close(fig)
            return save_path
        return ""