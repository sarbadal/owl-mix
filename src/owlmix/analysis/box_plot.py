import json
import math
import pandas as pd
from dataclasses import dataclass
from typing import Any, List, Dict, Optional
from tabulate import tabulate

from .base import BaseAnalyzer
from ..utils.mixin import ColumnMixin


@dataclass
class BoxParams:
    """
    Parameters for Box Plot analysis.

    Attributes:
        columns : Optional[List[str]]
            List of column names to include in the box plot analysis. 
            If None, all numeric columns are used.
        method : str
            Method to identify outliers. Options are 'iqr' (Interquartile Range) 
            and 'zscore' (Z-score method). Default is 'iqr'.
        threshold : float
            Threshold for identifying outliers. For 'iqr', it's the multiplier 
            for the IQR (default 1.5). For 'zscore', it's the Z-score threshold (default 3.0).
        precision : int
            Number of decimal places to round the statistics. Default is 2.
    """
    columns: Optional[List[str]] = None
    method: str = 'iqr'
    threshold: float | None = 1.5
    precision: int = 2

    def set_default_threshold(self):
        if self.threshold is None:
            self.threshold = 1.5 if self.method == 'iqr' else 3.0

    def __post_init__(self):
        if self.method not in ['iqr', 'zscore']:
            raise ValueError(f"Unsupported method: {self.method}. Supported methods are 'iqr' and 'zscore'.")
        if self.precision < 0:
            raise ValueError("Precision must be a non-negative integer.")


class BoxPlotAnalyzer(BaseAnalyzer, ColumnMixin):
    """
    Analyzer for creating box plot data from a DataFrame.

    This class computes the necessary statistics for creating box plots for the specified columns.

    Parameters:
        df : pd.DataFrame
            The input DataFrame containing the data.
        params : BoxParams
            The parameters for box plot analysis.
    Attributes:
        columns : List[str]
            List of column names to include in the box plot analysis.
    Methods:
        compute() -> Dict[str, Dict[str, float]]
            Compute the statistics for box plots for each selected column.
        print_results_json(results: list[dict], indent: int)
            Print the results in JSON format.
        print_results(results: dict)
            Print the results in a human-readable tabular format.
    Returns:
        Dict[str, Dict[str, float]]: 
            A dictionary where keys are column names and values are dictionaries 
            containing box plot statistics (min, Q1, median, Q3, max, mean, outliers).
    """
    def __init__(self, df: pd.DataFrame, params: BoxParams):
        super().__init__(df, params)
        self.columns = self._get_numeric_columns(params.columns)

    def _identify_outliers(self, col: str) -> List[int]:
        if self.params.method not in ['iqr', 'zscore']:
            raise ValueError(f"Unsupported method: {self.params.method}")
        
        if self.params.method == 'iqr':
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - self.params.threshold * IQR
            upper_bound = Q3 + self.params.threshold * IQR
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)][col].tolist()
            return [round(float(outlier), self.params.precision) for outlier in outliers]
        
        if self.params.method == 'zscore':
            mean = self.df[col].mean()
            std = self.df[col].std()
            z_scores = (self.df[col] - mean) / std
            outliers = self.df[abs(z_scores) > self.params.threshold][col].tolist()
            return [round(float(outlier), self.params.precision) for outlier in outliers]

        raise AssertionError("Unreachable: method validated above")

    def compute(self) -> List[Dict[str, Any]]:
        """
        Compute the statistics for box plots for each selected column.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries where each dictionary contains box plot statistics for a column.
            containing box plot statistics (min, Q1, median, mean, Q3, max, outliers).
        """
        results: List[Dict[str, Any]] = []
        for col in self.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                outliers = self._identify_outliers(col)
                stats = {
                    'column': col,
                    'min': round(float(self.df[col].min()), self.params.precision), 
                    'Q1': round(float(self.df[col].quantile(0.25)), self.params.precision), 
                    'median': round(float(self.df[col].median()), self.params.precision), 
                    "mean": round(float(self.df[col].mean()), self.params.precision),
                    'Q3': round(float(self.df[col].quantile(0.75)), self.params.precision), 
                    'max': round(float(self.df[col].max()), self.params.precision),
                    'outliers_count': len(outliers),
                    'outliers': outliers
                }
                results.append(stats)
        return results

    def print_results_json(self, results: List[Dict[str, Any]] | None = None, indent: int = 2) -> None:
        """
        Print the results in JSON format.

        Args:
            results (list[dict], optional): 
                The results to print. If None, uses the computed box plot statistics.
            indent (int): The indentation level for pretty-printing the JSON.
        """        
        if results is None:
            results = self.compute()
        print(json.dumps(results, indent=indent))

    def print_results(self, results: List[Dict[str, Any]] | None = None, include_outliers: bool = False) -> None:
        """
        Print the results in a human-readable tabular format.

        Args:
            results (list[dict], optional): The results to print. If None, uses the computed box plot statistics.
        """        
        if results is None:
            results = self.compute()
        table = []
        for stats in results:
            result =[
                stats['column'],
                stats['min'],
                stats['Q1'],
                stats['median'],
                stats['mean'],
                stats['Q3'],
                stats['max'],
                stats['outliers_count']
            ]
            if include_outliers:
                result.append(stats['outliers'])
            table.append(result)
        headers = ['Column', 'Min', 'Q1', 'Median', 'Mean', 'Q3', 'Max', 'Outliers Count']
        colalign = ["left", "right", "right", "right", "right", "right", "right", "right"]
        if include_outliers:
            headers.append('Outliers')
            colalign.append("left")
        print(tabulate(table, headers=headers, tablefmt='simple', colalign=colalign))


@dataclass
class BoxPlotData:
    """Data structure for Box Plot analysis results."""
    column: str
    min: float
    Q1: float
    median: float
    mean: float
    Q3: float
    max: float
    outliers_count: int
    outliers: List[float]

@dataclass
class PlotConfig:
    width: int = 400
    height: int = 120
    padding_px: int = 10
    padding_ratio: float = 0.01
    n_ticks: int = 5
    show_outliers: bool = True


@dataclass
class BoxPlotScalerConfig:
    """Configuration for Box Plot analysis."""
    data: BoxPlotData
    plot: PlotConfig


def build_box_plot_scaler_config(data: BoxPlotData, plot_config: PlotConfig | None = None) -> BoxPlotScalerConfig:
    """Helper function to build BoxPlotScalerConfig from BoxPlotData and PlotConfig."""
    if plot_config is None:
        plot_config = PlotConfig()

    if not isinstance(data, BoxPlotData):
        data = BoxPlotData(**data)
    return BoxPlotScalerConfig(data=data, plot=plot_config)


class BoxPlotScaler:
    """This class can be implemented to scale the box plot statistics for better 
    visualization or comparison across different columns."""
    def __init__(self, config: BoxPlotScalerConfig):
        self.config = config
        self.domain_min: float = 0.0
        self.domain_max: float = 0.0
        self.tick_step: float = 0.0

    def compute_domain(self):
        all_values = [self.config.data.min, self.config.data.max] + self.config.data.outliers
        self.domain_min = min(all_values)
        self.domain_max = max(all_values)

    def apply_padding(self):
        span = self.domain_max - self.domain_min
        if span == 0:
            span = abs(self.domain_min) if self.domain_min != 0 else 1
        padding = span * self.config.plot.padding_ratio + self.config.plot.padding_px
        self.domain_min -= padding
        self.domain_max += padding

    def compute_ticks(self):
        nice_range = self._nice_number(self.domain_max - self.domain_min, round_=False)
        step = self._nice_number(nice_range / (self.config.plot.n_ticks - 1), round_=True)

        tick_min = math.floor(self.domain_min / step) * step
        tick_max = math.ceil(self.domain_max / step) * step

        ticks = []
        v = tick_min
        while v <= tick_max + 1e-9:  # Adding a small epsilon to account for floating-point precision
            ticks.append(v)
            v += step

        self.domain_min = tick_min
        self.domain_max = tick_max
        self.tick_step = step
        return ticks

    def compute_tick_(self):
        raw_min = self.domain_min
        raw_max = self.domain_max

        nice_range = self._nice_number(raw_max - raw_min, round_=False)
        step = self._nice_number(nice_range / (self.config.plot.n_ticks - 1), round_=True)

        # Start from data whiskers instead of padded domain to avoid wide empty tails
        data_min = self.config.data.min
        data_max = self.config.data.max
        q1 = self.config.data.Q1
        q3 = self.config.data.Q3
        iqr = max(q3 - q1, step)

        tick_min = math.floor(data_min / step) * step
        tick_max = math.ceil(data_max / step) * step

        # Keep axis endpoints reasonably close to the box (Q1/Q3),
        # but never clip the actual min/max.
        # max_side_gap = max(step, 0.6 * iqr)
        max_side_gap = max(1 * step, 1.1 * iqr)

        while (q1 - tick_min) > max_side_gap and (tick_min + step) <= data_min:
            tick_min += step

        while (tick_max - q3) > max_side_gap and (tick_max - step) >= data_max:
            tick_max -= step

        ticks = []
        v = tick_min
        while v <= tick_max + 1e-9:
            ticks.append(v)
            v += step

        self.domain_min = tick_min
        self.domain_max = tick_max
        self.tick_step = step
        return ticks

    def _format_label(self, val: float) -> str:
        if abs(val) < 1:
            return f"{val:.2f}"
        if abs(val) < 10:
            return f"{val:.1f}"
        return f"{val:.0f}"

    def _nice_number(self, value: float, round_: bool = True) -> float:
        exponent = math.floor(math.log10(value))
        fraction = value / (10 ** exponent)
        if round_:
            if fraction < 1.5:
                nice_fraction = 1
            elif fraction < 3:
                nice_fraction = 2
            elif fraction < 7:
                nice_fraction = 5
            else:
                nice_fraction = 10
        else:
            if fraction <= 1:
                nice_fraction = 1
            elif fraction <= 2:
                nice_fraction = 2
            elif fraction <= 5:
                nice_fraction = 5
            else:
                nice_fraction = 10
        return nice_fraction * (10 ** exponent)

    def scale(self, value: float) -> float:
        """Scale the box plot data based on the provided configuration."""
        return self.config.plot.padding_px + (
            (value - self.domain_min) * (self.config.plot.width - 2 * self.config.plot.padding_px)
            / (self.domain_max - self.domain_min)
        )

    def build(self):
        self.compute_domain()
        self.apply_padding()
        tick_values = self.compute_ticks()

        result = {
            "x": self.config.data.column,
            "x_min": self.scale(self.config.data.min),
            "x_q1": self.scale(self.config.data.Q1),
            "x_median": self.scale(self.config.data.median),
            "x_mean": self.scale(self.config.data.mean),
            "x_q3": self.scale(self.config.data.Q3),
            "x_max": self.scale(self.config.data.max),
            "x_outliers": [self.scale(v) for v in self.config.data.outliers],
        }

        ticks = []
        for v in tick_values:
            ticks.append({
                "value": v,
                "label": self._format_label(v),
                "x": self.scale(v)
            })

        result.update({
            "domain_min": self.domain_min,
            "domain_max": self.domain_max,
            "ticks": ticks
        })
 
        return result

    def print_results_json(self, results: dict[str, Any] | None = None, indent: int = 2) -> None:
        """
        Print the results in JSON format.

        Args:
            results (list[dict], optional): 
                The results to print. If None, uses the computed box plot statistics.
            indent (int): The indentation level for pretty-printing the JSON.
        """        
        if results is None:
            results = self.build()
        print(json.dumps(results, indent=indent))

    def print_results(self, results: dict[str, Any] | None = None, include_outliers: bool = False) -> None:
        """
        Print the results in a human-readable tabular format.

        Args:
            results (list[dict], optional): The results to print. If None, uses the computed box plot statistics.
        """        
        if results is None:
            results = self.build()
        table = []
        stats = results
        result =[
            stats['x'],
            stats['x_min'],
            stats['x_q1'],
            stats['x_median'],
            stats['x_mean'],
            stats['x_q3'],
            stats['x_max'],
            stats['domain_min'],
            stats['domain_max']
        ]
        
        headers = ['Column', 'Min', 'Q1', 'Median', 'Mean', 'Q3', 'Max', 'Domain Min', 'Domain Max']
        colalign = ["left", "right", "right", "right", "right", "right", "right", "right", "right"]

        if include_outliers:
            result.append(", ".join([str(round(float(v), 2)) for v in stats['x_outliers']]))
            headers.append('Outliers')
            colalign.append("left")
        table.append(result)
        print(tabulate(table, headers=headers, tablefmt='simple', colalign=colalign))


def box_plot_scaler(data: list[BoxPlotData], plot_config: PlotConfig | None = None) -> list[dict[str, Any]]:
    """Helper function to compute scaled box plot data from BoxPlotData and PlotConfig."""
    results = []
    for item in data:
        config = build_box_plot_scaler_config(data=item, plot_config=plot_config)
        scaler = BoxPlotScaler(config=config)
        result = scaler.build()
        results.append(result)

    return results