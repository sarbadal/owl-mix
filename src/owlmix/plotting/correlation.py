import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from .base import BasePlotter


@dataclass
class CorrPlotParams:
    ...


class CorrelationPlotter(BasePlotter):

    def __init__(self, data: Dict[str, Dict[str, Any]], params: CorrPlotParams | None = None):
        super().__init__(data, params or CorrPlotParams())

    def generate(self, output_dir: str = "outputs/charts") -> Tuple[str, str]:
        self.output_dir = output_dir
        corr_file_path = self.plot_correlation_matrix(self.data.get("correlation_matrix", {}))
        lagged_corr_file_path = self.plot_lagged_correlation_matrix(self.data.get("lagged_correlation_matrix", {}))
        return corr_file_path, lagged_corr_file_path

    def plot_correlation_matrix(self, corr_matrix: Dict[str, Dict[str, float]]) -> str:
        if not corr_matrix:
            print("Empty correlation matrix.")
            return ""

        # Convert nested dict to DataFrame
        df = pd.DataFrame(corr_matrix)
        # Ensure symmetry (optional, for safety)
        df = df.reindex(index=df.index, columns=df.columns, fill_value=0)

        plt.figure(figsize=(8, 6))
        sns.heatmap(df, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
        plt.title("Correlation Matrix")

        os.makedirs(self.output_dir, exist_ok=True)
        file_path = os.path.join(self.output_dir, "corr_matrix.png")

        plt.tight_layout()
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        return file_path

    def plot_lagged_correlation_matrix(self, lag_corr: Dict[str, Dict[int, float]]) -> str:
        if not lag_corr:
            print("Empty lagged correlation matrix.")
            return ""

        # Convert nested dict to DataFrame
        df = pd.DataFrame(lag_corr)
        # Ensure symmetry (optional, for safety)
        df = df.reindex(index=df.index, columns=df.columns, fill_value=0)

        plt.figure(figsize=(8, 6))
        sns.heatmap(df, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
        plt.title("Lagged Correlation Matrix")

        os.makedirs(self.output_dir, exist_ok=True)
        file_path = os.path.join(self.output_dir, "lagged_corr_matrix.png")

        plt.tight_layout()
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        return file_path