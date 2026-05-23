import json
import numpy as np
import pandas as pd
from scipy.stats import norm
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from tabulate import tabulate

from .base import BaseAnalyzer
from ..utils.mixin import ColumnMixin


@dataclass
class NumericalDistributionParams:
    columns: Optional[List[str]] = None
    precision: int = 3
    bins: int = 30


class NumericalDistributionAnalysis(BaseAnalyzer, ColumnMixin):
    def __init__(self, df: pd.DataFrame, params: NumericalDistributionParams):
        super().__init__(df, params)
        self.columns = self._get_numeric_columns(params.columns)
        self.precision = params.precision
        self.bins = params.bins

    def _compute_bins(self, column: str) -> Dict[str, Any]:
        data = self.df[column].dropna().to_numpy(dtype=float)

        if data.size == 0:
            return {
                "column": column,
                "bin_count": 0,
                "bins": [],
                "normal_fit": {"mu": None, "std": None, "x": [], "y": []}
            }

        density_y, edges = np.histogram(data, bins=self.bins, density=True)
        counts, _ = np.histogram(data, bins=edges, density=False)
        centers = 0.5 * (edges[:-1] + edges[1:])

        mu, std = norm.fit(data)
        curve_x = np.linspace(edges[0], edges[-1], 100)

        if std == 0:
            curve_y = np.zeros_like(curve_x)
        else:
            curve_y = norm.pdf(curve_x, mu, std)

        p = self.precision
        bins_payload = []
        for i in range(len(density_y)):
            bins_payload.append({
                "left": round(float(edges[i]), p),
                "right": round(float(edges[i + 1]), p),
                "center": round(float(centers[i]), p),
                "count": int(counts[i]),
                "y": round(float(density_y[i]), p)  # histogram height (density)
            })

        return {
            "column": column,
            "bin_count": len(bins_payload),
            "bins": bins_payload,
            "normal_fit": {
                "mu": round(float(mu), p),
                "std": round(float(std), p),
                "x": [round(float(v), p) for v in curve_x],
                "y": [round(float(v), p) for v in curve_y]
            }
        }

    def compute(self) -> List[Dict[str, Any]]:
        return [self._compute_bins(col) for col in self.columns]

    def print_results_json(self, results: Optional[List[Dict[str, Any]]] = None, indent: int = 2) -> None:
        if results is None:
            results = self.compute()
        print(json.dumps(results, indent=indent))

    def print_results(self, results: Optional[List[Dict[str, Any]]] = None) -> None:
        if results is None:
            results = self.compute()

        table = []
        for col_result in results:
            for b in col_result["bins"]:
                table.append([
                    col_result["column"],
                    b["left"],
                    b["right"],
                    b["center"],
                    b["count"],
                    b["y"],
                ])

        headers = ["Column", "Bin Left", "Bin Right", "Center", "Count", "Y (Density)"]
        print(tabulate(table, headers=headers, tablefmt="simple"))