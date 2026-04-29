# owlmix/eda/summary_builder_config.py
"""
Summary Builder Configuration Module

This module defines the configuration schema and management logic for the
OwlMix EDA process. It provides a centralized way to manage parameters for
various statistical tests and visualization layouts.

The `SummaryBuilderConfig` class uses a fluent interface (method chaining)
and type-safe `TypedDict` structures to configure:
- **Statistical Tests**: VIF (Multicollinearity), Granger Causality, and ACF/PACF.
- **Time Analysis**: KPI vs. Feature comparisons and time-series aggregations.
- **Visualizations**: Correlation heatmaps and outlier chart layouts.
- **Data Schemas**: Target column, date column, and categorical variable mapping.

By decoupling configuration from the execution logic, this module ensures
consistency across the JSON and HTML reporting workflows.
"""

import pandas as pd
from dataclasses import replace
from typing import Self, Unpack

from ..typing.types import PeriodType, ComparisonType, PlotModeType

from .args import Args
from .args import SetAcfPacfConfigArgs
from .args import SetCategoricalColumnsConfigArgs
from .args import SetCausalityTestConfigArgs
from .args import SetCorrChartLayoutConfigArgs
from .args import SetCorrelationConfigArgs
from .args import SetKPIVsFeatureConfigArgs
from .args import SetOutlierConfigArgs
from .args import SetTimeAggregatorConfigArgs
from .args import SetTimeComparisonChartConfigArgs
from .args import SetTimeComparisonConfigArgs
from .args import SetVIFConfigArgs


class SummaryBuilderConfig:

    def __init__(self, df: pd.DataFrame, target: str, date_column: str):
        self.df = df
        self.target = target
        self.date_column = date_column
        self.init_config()

    def init_config(self) -> None:
        """Initialize all configuration dictionaries with defaults."""
        self.correlation_chart_layout_config = Args.corr_chart_layout.build()
        self.correlation_config = Args.correlation.build()
        self.vif_config = Args.vif.build(target_column=self.target)
        self.acf_pacf_config = Args.acf_pacf.build(columns=[self.target])
        self.categorical_columns_config = Args.categorical_columns.build()
        self.kpi_vs_feature_config = Args.kpi_vs_feature.build(target_column=self.target, date_column=self.date_column)
        self.causality_test_config = Args.causality_test.build(target_column=self.target, date_column=self.date_column)

        self.outlier_chart_layout_config = {
            "columns": None,
            "max_cols_per_chart": 4,
            "single_image": True
        }

        self.time_comparison_config = {
            "date_column": self.date_column,
            "value_columns": None,
            "comparison_type": "yoy",
            "agg_func": "sum",
            "precision": 2,
            "freq": "ME"
        }

        self.time_comparison_chart_config = {
            "date_column": self.date_column,
            "value_columns": None,
            "comparison_type": "yoy",
            "agg_func": "sum",
            "mode": "pct_change"
        }

        self.time_aggregator_config = {
            "date_column": self.date_column,
            "value_columns": None,
            "agg_func": "sum",
            "freq": "YE",
            "precision": 2
        }

        self.time_series_config = {
            "columns": self.target
        }

    def _validate_positive_int(self, value: Any, field_name: str) -> None:
        """Validate that a value is a positive integer."""
        if value is not None and (not isinstance(value, int) or value < 1):
            raise ValueError(f"{field_name} must be a positive integer")

    def _update_config(self, config: dict, updates: dict, defaults: dict | None = None) -> None:
        """Update a config dictionary with provided values, preserving existing values if not provided."""
        defaults = defaults or {}

        for key, value in updates.items():
            if value is not None:
                config[key] = value
            elif key in defaults and config[key] is None:
                config[key] = defaults[key]

    def set_causality_test_config(self, **kwargs: Unpack[SetCausalityTestConfigArgs]) -> Self:
        self.causality_test_config = replace(self.causality_test_config, **kwargs)
        return self

    def set_vif_config_(self, **kwargs: Unpack[SetVIFConfigArgs]) -> Self:
        """
        Set VIF configuration.

        Args:
            target_column: str - target column name
            features: list[str] - features to analyze
            precision: int - decimal precision for results
        """
        precision = kwargs.get("precision", 3)
        self._validate_positive_int(precision, "precision")

        updates = {
            "target_column": kwargs.get("target_column"),
            "features": kwargs.get("features"),
            "precision": precision
        }
        self._update_config(self.vif_config, updates)
        return self

    def set_vif_config(self, **kwargs: Unpack[SetVIFConfigArgs]) -> Self:
        self.vif_config = replace(self.vif_config, **kwargs)
        return self

    def set_kpi_vs_feature_config(self, **kwargs: Unpack[SetKPIVsFeatureConfigArgs]) -> Self:
        self.kpi_vs_feature_config = replace(self.kpi_vs_feature_config, **kwargs)
        return self

    def set_acf_pacf_config_(self, **kwargs: Unpack[SetAcfPacfConfigArgs]) -> Self:
        """
        Set ACF/PACF configuration.

        Args:
            columns: list[str] - columns for analysis
            n_lags: int - number of lags
        """
        updates = {
            "columns": kwargs.get("columns") or [self.target],
            "n_lags": kwargs.get("n_lags", 15)
        }
        self._update_config(self.acf_pacf_config, updates)
        return self

    def set_acf_pacf_config(self, **kwargs: Unpack[SetAcfPacfConfigArgs]) -> Self:
        self.acf_pacf_config = replace(self.acf_pacf_config, **kwargs)
        return self

    def set_correlation_config_(self, **kwargs: Unpack[SetCorrelationConfigArgs]) -> Self:
        """
        Set Correlation configuration.

        Args:
            columns: list[str] - columns for correlation analysis
        """
        updates = {"columns": kwargs.get("columns")}
        self._update_config(self.correlation_config, updates)
        return self

    def set_correlation_config(self, **kwargs: Unpack[SetCorrelationConfigArgs]) -> Self:
        self.correlation_config = replace(self.correlation_config, **kwargs)
        return self

    def set_time_series_config(self, **kwargs) -> Self:
        """
        Set Time Series configuration.

        Args:
            columns: str or list[str] - columns for time series
        """
        updates = {"columns": kwargs.get("columns")}
        self._update_config(self.time_series_config, updates)
        return self

    def set_time_comparison_config(self, **kwargs: Unpack[SetTimeComparisonConfigArgs]) -> Self:
        """
        Set Time Comparison configuration.

        Args:
            date_column: str - date column name
            value_columns: list[str] - columns to compare
            comparison_type: str - type of comparison (yoy, mom, etc.)
            agg_func: str - aggregation function
            precision: int - decimal precision
            freq: str - frequency (ME=month-end, etc.)
        """
        precision = kwargs.get("precision", 2)
        self._validate_positive_int(precision, "precision")

        updates = {
            "date_column": kwargs.get("date_column") or self.date_column,
            "value_columns": kwargs.get("value_columns"),
            "comparison_type": kwargs.get("comparison_type", "yoy"),
            "agg_func": kwargs.get("agg_func", "sum"),
            "precision": precision
        }
        self._update_config(self.time_comparison_config, updates)
        return self

    def set_time_comparison_chart_config(self, **kwargs: Unpack[SetTimeComparisonChartConfigArgs]) -> Self:
        """
        Set Time Comparison chart configuration.

        Args:
            date_column: str - date column name
            value_columns: list[str] - columns to compare
            comparison_type: str - type of comparison (yoy, mom, etc.)
            agg_func: str - aggregation function
            mode: str - absolute, pct_change, dual
        """
        precision = kwargs.get("precision", 2)
        self._validate_positive_int(precision, "precision")

        updates = {
            "date_column": kwargs.get("date_column") or self.date_column,
            "value_columns": kwargs.get("value_columns"),
            "comparison_type": kwargs.get("comparison_type", "yoy"),
            "agg_func": kwargs.get("agg_func", "sum"),
            "mode": kwargs.get("mode", "absolute")
        }
        self._update_config(self.time_comparison_chart_config, updates)
        return self

    def set_time_aggregator_config(self, **kwargs: Unpack[SetTimeAggregatorConfigArgs]) -> Self:
        """
        Set Time Aggregator configuration.

        Args:
            date_column: str - date column name
            value_columns: list[str] - columns to aggregate
            agg_func: str - aggregation function
            freq: str - frequency (YE=year-end, etc.)
            precision: int - decimal precision
        """
        precision = kwargs.get("precision", 2)
        self._validate_positive_int(precision, "precision")

        updates = {
            "date_column": kwargs.get("date_column") or self.date_column,
            "value_columns": kwargs.get("value_columns"),
            "agg_func": kwargs.get("agg_func", "sum"),
            "freq": kwargs.get("freq", "YE"),
            "precision": precision
        }
        self._update_config(self.time_aggregator_config, updates)
        return self

    def set_outlier_chart_layout_config(self, **kwargs: Unpack[SetOutlierConfigArgs]) -> Self:
        """
        Set Outlier Chart Layout configuration.

        Args:
            columns: list[str] - columns to analyze
            max_cols_per_chart: int - maximum columns per chart
            single_image: bool - whether to use single image
        """
        max_cols = kwargs.get("max_cols_per_chart", 4)
        self._validate_positive_int(max_cols, "max_cols_per_chart")

        updates = {
            "columns": kwargs.get("columns"),
            "max_cols_per_chart": max_cols,
            "single_image": kwargs.get("single_image", True)
        }
        self._update_config(self.outlier_chart_layout_config, updates)
        return self

    def set_correlation_chart_layout_config(self, **kwargs: Unpack[SetCorrChartLayoutConfigArgs]) -> Self:
        self.correlation_chart_layout_config = replace(self.correlation_chart_layout_config, **kwargs)
        return self

    def set_categorical_columns_config(self, **kwargs: Unpack[SetCategoricalColumnsConfigArgs]) -> Self:
        self.categorical_columns_config = replace(self.categorical_columns_config, **kwargs)
        return self