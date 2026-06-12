import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from scipy.stats import norm

from .base import BasePlotter
from ..utils.mixin import ColumnMixin


@dataclass
class NumericalDistributionPlotParams:
    columns: Optional[List[str]] = None
    show_normal_curve: bool = True
    dpi: int = 150
    figsize: tuple[float, float] = (6.0, 4.0)
    filename_prefix: str = "distribution"


class NumericalDistributionPlotter(ColumnMixin):
    """
    Plotter that consumes NumericalDistributionAnalysis.compute() output only.
    No DataFrame input, no recomputation.
    """

    def __init__(self, df: pd.DataFrame, params: NumericalDistributionPlotParams | None = None):
        self.df = df.copy()
        self.params = params or NumericalDistributionPlotParams()
        self.columns = self._get_numeric_columns(self.params.columns)

    def _safe_name(self, value: str) -> str:
        _name = re.sub(r"[^A-Za-z0-9._-]+", "_", str(value)).strip("_")
        return _name

    def _plot(self, col: str, output_dir: str) -> str | None:
        fig, ax = plt.subplots()
        data = self.df[col].dropna().to_numpy(dtype=float)
        if len(data) == 0:
            return None

        ax.hist(data, bins=30, density=True, alpha=0.6, color='g')

        if self.params.show_normal_curve:
            mu, std = norm.fit(data)
            xmin, xmax = ax.get_xlim()
            x = np.linspace(xmin, xmax, 100)
            p = norm.pdf(x, mu, std)
            ax.plot(x, p, 'k', linewidth=2)

        ax.set_title(f"Distribution of {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Density")
        file_path = os.path.join(output_dir, f"{self.params.filename_prefix}_{self._safe_name(col)}.png")
        self._save_figure(fig, file_path, col)
        return file_path

    def _save_figure(self, fig: plt.Figure, output_path: str, col: str) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fig.savefig(
            output_path, 
            dpi=self.params.dpi,
            bbox_inches="tight",
            transparent=True
        )
        plt.close(fig)
        return output_path

    def plot(self, output_dir: str = "outputs/charts") -> Dict[str, str]:
        """
        Expects self.data exactly as returned by NumericalDistributionAnalysis.compute().
        Returns mapping: {column_name: file_path}
        """
        os.makedirs(output_dir, exist_ok=True)
        saved: Dict[str, str] = {}

        for column in self.columns:
            path = self._plot(column, output_dir)
            if path is not None:
                saved[column] = path
        return saved