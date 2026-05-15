import json
import pandas as pd
from typing import List, Dict, Optional
from dataclasses import dataclass
from tabulate import tabulate

from .base import BaseAnalyzer
from ..utils.mixin import ColumnMixin


@dataclass
class BoxPlotParams:
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
    threshold: float | None = None
    precision: int = 2

    def __post_init__(self):
        if self.method not in ['iqr', 'zscore']:
            raise ValueError(f"Unsupported method: {self.method}. Supported methods are 'iqr' and 'zscore'.")
        if self.precision < 0:
            raise ValueError("Precision must be a non-negative integer.")
        if self.threshold is None:
            self.threshold = 1.5 if self.method == 'iqr' else 3.0


class BoxPlotAnalyzer(BaseAnalyzer, ColumnMixin):
    """
    Analyzer for creating box plot data from a DataFrame.

    This class computes the necessary statistics for creating box plots for the specified columns.

    Parameters:
        df : pd.DataFrame
            The input DataFrame containing the data.
        params : BoxPlotParams
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
            containing box plot statistics (min, Q1, median, Q3, max, outliers).
    """
    def __init__(self, df: pd.DataFrame, params: BoxPlotParams):
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

    def compute(self) -> Dict[str, Dict[str, float]]:
        """
        Compute the statistics for box plots for each selected column.

        Returns:
            Dict[str, Dict[str, float]]: A dictionary where keys are column names and values are dictionaries
            containing box plot statistics (min, Q1, median, Q3, max, outliers).
        """
        results: List[Dict[str, float]] = []
        for col in self.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                outliers = self._identify_outliers(col)
                stats = {
                    'column': col,
                    'min': round(float(self.df[col].min()), self.params.precision), 
                    'Q1': round(float(self.df[col].quantile(0.25)), self.params.precision), 
                    'median': round(float(self.df[col].median()), self.params.precision), 
                    'Q3': round(float(self.df[col].quantile(0.75)), self.params.precision), 
                    'max': round(float(self.df[col].max()), self.params.precision),
                    'outliers_count': len(outliers),
                    'outliers': outliers
                }
                results.append(stats)
        return results

    def print_results_json(self, results: list[dict] = None, indent: int = 2) -> None:
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

    def print_results(self, results: list[dict] = None, include_outliers: bool = False) -> None:
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
                stats['Q3'],
                stats['max'],
                stats['outliers_count']
            ]
            if include_outliers:
                result.append(stats['outliers'])
            table.append(result)
        headers = ['Column', 'Min', 'Q1', 'Median', 'Q3', 'Max', 'Outliers Count']
        colalign = ["left", "right", "right", "right", "right", "right", "right"]
        if include_outliers:
            headers.append('Outliers')
            colalign.append("left")
        print(tabulate(table, headers=headers, tablefmt='simple', colalign=colalign))