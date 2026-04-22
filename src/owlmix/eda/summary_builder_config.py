# owlmix/eda/summary_builder_config.py
import pandas as pd
from typing import Self


class SummaryBuilderConfig:

    def __init__(self, df: pd.DataFrame, target: str, date_column: str):
        self.df = df
        self.target = target
        self.date_column = date_column

        self.outlier_chart_config = {
            "columns": None,
            "max_cols_per_chart": 4,
            "single_image": True
        }

        self.correlation_chart_config = {
            "columns": None,
            "precision": 2
        }

        self.correlation_config = {
            "columns": None
        }

        self.time_comparison_config = {
            "value_columns": None,
            "comparison_type": "yoy",
            "agg_func": "sum",
            "precision": 2
        }

        self.vif_config = {
            "target_column": self.target,
            "features": None,
            "precision": 3
        }

        self.acf_pacf_config = {
            "columns": [self.target],
            "n_lags": 15
        }

        self.categorical_columns = {
            "columns": None
        }

        self.kpi_vs_feature_config = {
            "target_column": self.target,
            "columns": None,
            "date_format": "%Y-%m-%d",
            "date_column": self.date_column,
            "agg_func": "sum",
        }

    def set_vif_config(self, target_column: str = None, features: list[str] = None, precision: int = 3) -> Self:
        if not isinstance(precision, int) or precision < 1:
            raise ValueError("precision must be a positive integer")

        self.vif_config["target_column"] = target_column
        self.vif_config["features"] = features
        self.vif_config["precision"] = precision

        return self

    def set_kpi_vs_feature_config(self, target_column: str = None, columns: list[str] = None, date_column: str = None, date_format: str = "%Y-%m-%d", agg_func: str = "sum") -> Self:
        self.kpi_vs_feature_config["target_column"] = target_column or self.target
        self.kpi_vs_feature_config["date_format"] = date_format
        self.kpi_vs_feature_config["date_column"] = date_column or self.date_column
        self.kpi_vs_feature_config["agg_func"] = agg_func
        self.kpi_vs_feature_config["columns"] = columns

        return self

    def set_acf_pacf_config(self, columns: list[str] = None, n_lags: int = 15) -> Self:
        self.acf_pacf_config["columns"] = columns or [self.target]
        self.acf_pacf_config["n_lags"] = n_lags

        return self

    def set_correlation_config(self, columns: list[str] = None) -> Self:
        self.correlation_config["columns"] = columns

        return self

    def set_time_comparison_config(self, date_column: str = None, value_columns: list[str] = None, comparison_type: str = "yoy", agg_func: str = "sum", precision: int = 2) -> Self:
        self.is_precision_valid(precision)

        self.time_comparison_config["date_column"] = date_column if date_column else self.date_column
        self.time_comparison_config["value_columns"] = value_columns
        self.time_comparison_config["comparison_type"] = comparison_type
        self.time_comparison_config["agg_func"] = agg_func
        self.time_comparison_config["precision"] = precision

        return self

    def set_outlier_chart_layout(self, columns: list[str] = None, max_cols_per_chart: int = 4, single_image: bool = True) -> Self:
        if not isinstance(max_cols_per_chart, int) or max_cols_per_chart < 1:
            raise ValueError("max_cols_per_chart must be a positive integer")

        self.outlier_chart_config["max_cols_per_chart"] = max_cols_per_chart
        self.outlier_chart_config["single_image"] = single_image
        self.outlier_chart_config["columns"] = columns

        return self

    def set_correlation_chart_layout(self, columns: list[str] = None, precision: int = 2):
        self.is_precision_valid(precision)

        self.correlation_chart_config["columns"] = columns
        self.correlation_chart_config["precision"] = precision

        return self

    def set_categorical_columns(self, columns: list[str] = None) -> Self:
        self.categorical_columns["columns"] = columns

        return self

    def is_precision_valid(self, precision: int) -> Self:
        if not isinstance(precision, int) or precision < 1:
            raise ValueError("precision must be a positive integer")