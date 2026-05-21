import json
import numpy as np
import pandas as pd
from typing import List, Dict, Optional
from dataclasses import dataclass
from tabulate import tabulate

from .base import BaseAnalyzer
from ..utils.mixin import ColumnMixin
from .transformer.difference import DifferenceTransformer
from .transformer.lag import LagTransformer
from .transformer.adstock import AdstockTransformer
from .transformer.base import BaseTransformer


adstock_transformer = AdstockTransformer(decay_rate=0.5)
diff_transformer = DifferenceTransformer(period=1)
lag_transformer = LagTransformer(lag=1)

TRANSFORMER_FACTORIES = {
    "adstock": lambda: AdstockTransformer(decay_rate=0.5),
    "difference": lambda: DifferenceTransformer(period=1),
    "lag": lambda: LagTransformer(lag=1),
}

TRANSFORMERS = ["adstock", "difference", "lag"]


@dataclass
class CCFParams:
    """Parameters for Cross-Correlation Function (CCF) analysis.

    Attributes:
        time_column : Optional[str]
            The name of the time column in the DataFrame. If None, the index 
            is used as the time column.
        target_column : Optional[str]
            The name of the target column for which to compute the CCF. 
            If None, the first numeric column is used as the target column.
        feature_columns : Optional[List[str]]
            List of column names to include as features in the CCF analysis. 
            If None, all numeric columns except the target column are 
            used as feature columns.
        max_lag : int
            The maximum lag to compute for the CCF analysis. The CCF will be 
            computed for lags from -max_lag to max_lag.
    """
    time_column: Optional[str] = None
    target_column: Optional[str] = None
    feature_columns: Optional[List[str]] = None
    max_lag: int = 5


class CCFAnalyzer(BaseAnalyzer, ColumnMixin):
    """Analyzer for computing Cross-Correlation Function (CCF) between a target column and feature columns.

    This class computes the CCF between a target column and specified feature columns for a range of lags.

    Parameters:
        df : pd.DataFrame
            The input DataFrame containing the data.
        params : CCFParams
            The parameters for CCF analysis.
    """
    def __init__(self, df: pd.DataFrame, params: CCFParams, transformer: List[BaseTransformer] = None):
        super().__init__(df.copy(), params)
        self.feature_columns = self._get_numeric_columns(params.feature_columns)
        self.feature_columns = [
            col for col in self.feature_columns if col != self.params.target_column
        ]
        self.transformer = transformer if transformer is not None else TRANSFORMERS
        self.transformer = [self.transformer] if isinstance(self.transformer, str) else self.transformer
        self.ccf_results = {}
        self.summary_table = None

    def _get_feature_versions(self, feature: str) -> Dict[str, pd.Series]:
        """Generate different versions of the feature column for analysis.

        Args:
            feature (str): The name of the feature column.

        Returns:
            A dictionary containing different versions of the feature column, 
            such as original, adstocked, and differenced versions.
        """
        versions = {
            "original": self.df[feature].copy()
        }
        for transformer_name in self.transformer:
            factory = TRANSFORMER_FACTORIES.get(transformer_name)
            if factory:
                transformer = factory()
                transformed_series = transformer.transform(self.df[feature].copy())
                versions[transformer_name] = transformed_series
        return versions

    def compute(self) -> Dict[str, Dict[int, float]]:
        """Compute the CCF between the target column and feature columns for specified lags.

        Returns:
            A dictionary where keys are feature column names and values are dictionaries 
            mapping lag values to their corresponding CCF values.
        """
        all_results = []
        summary_rows = []

        for feature in self.feature_columns:
            versions = self._get_feature_versions(feature)

            for version_name, series in versions.items():
                ccf_df = self._compute_ccf_for_feature(feature, series, version_name)
                key = f"{feature}_{version_name}"
                self.ccf_results[key] = ccf_df
                all_results.append(ccf_df)
                valid_df = ccf_df.dropna()

                if not valid_df.empty:
                    max_corr_row = valid_df.loc[valid_df['correlation'].abs().idxmax()]
                    correlation_at_lag_0 = float(valid_df.loc[valid_df['lag'] == 0, 'correlation'].values[0])
                    summary_rows.append({
                        "target_column": self.params.target_column,
                        "feature": feature,
                        "version": version_name,
                        "max_correlation": round(max_corr_row['correlation'], 3),
                        "lag_at_max": int(max_corr_row['lag']),
                        "correlation_at_lag_0": correlation_at_lag_0
                    })
        self.summary_table = pd.DataFrame(summary_rows)
        return {
            "ccf_results": {feature: df.to_dict(orient='records') for feature, df in self.ccf_results.items()},
            "summary_table": self.summary_table.to_dict(orient='records')
        }

    def _compute_ccf_for_feature(self, feature: str, series: pd.Series, version_name: str) -> list[dict]:
        """Compute the CCF value for a given lag.

        Args:
            feature (str): The name of the feature column for which to compute the CCF.
            series (pd.Series): The series of the feature column to use for computation.
            version_name (str): The version of the feature column to use (e.g., "original", "adstocked", "differenced").

        Returns:
            The computed CCF value for the given lag.
        """
        results = []
        target_series = self.df[self.params.target_column].copy()

        for lag in range(0, self.params.max_lag + 1):
            shifted_feature = series.shift(lag)
            valid_idx = shifted_feature.notna() & target_series.notna()
            if valid_idx.sum() > 2:
                corr = np.corrcoef(shifted_feature[valid_idx], target_series[valid_idx])[0, 1]
            else:
                corr = np.nan

            results.append({
                "target_column": self.params.target_column,
                "feature": feature,
                "version": version_name,
                "lag": lag,
                "correlation": round(corr, 3) if not np.isnan(corr) else None
            })
        return pd.DataFrame(results)

    def print_results_json(self, results: list[dict] = None, indent: int = 2) -> None:
        """
        Print the results in JSON format.

        Args:
            results (list[dict], optional): The results to print. If None, uses the computed CCF results and summary table.
            indent (int): The indentation level for pretty-printing the JSON.
        """
        if results is None:
            results = {
                "target_column": self.params.target_column,
                "ccf_results": {feature: df.to_dict(orient='records') for feature, df in self.ccf_results.items()},
                "summary_table": self.summary_table.to_dict(orient='records') if self.summary_table is not None else None
            }
        print(json.dumps(results, indent=indent))

    def print_results(self, results: dict = None) -> None:
        """
        Print the results in a human-readable format.

        Args:
            results (dict, optional): The results to print. If None, uses the computed CCF results and summary table.
        """
        if results is None:
            results = self.compute()

        if self.ccf_results:
            combined_ccf_df = pd.concat(self.ccf_results.values(), ignore_index=True)
            print("Combined CCF Results for All Features:")
            print(tabulate(combined_ccf_df, headers='keys', tablefmt='simple', floatfmt=".3f", showindex=False))
            print("\n")
        else:
            print("No CCF results to display.\n")

        if self.summary_table is not None:
            print("Summary Table:")
            print(tabulate(self.summary_table, headers='keys', tablefmt='simple', floatfmt=".3f", showindex=False))