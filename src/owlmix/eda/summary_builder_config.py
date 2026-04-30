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
from .._deprecated import deprecated

from .args import Args
from .args import SetAcfPacfConfigArgs
from .args import SetCategoricalColumnsConfigArgs
from .args import SetCausalityTestConfigArgs
from .args import SetCorrChartLayoutConfigArgs
from .args import SetCorrelationConfigArgs
from .args import SetDistributionChartConfigArgs
from .args import SetKPIVsFeatureConfigArgs
from .args import SetOutlierConfigArgs
from .args import SetTimeAggregatorConfigArgs
from .args import SetTimeComparisonChartConfigArgs
from .args import SetTimeComparisonConfigArgs
from .args import SetTimeSeriesConfigArgs
from .args import SetVIFConfigArgs


class SummaryBuilderConfig:

    def __init__(self, df: pd.DataFrame, target: str, date_column: str):
        self.df = df
        self.target = target
        self.date_column = date_column
        self.init_config()

    def init_config(self) -> None:
        """Initialize all configuration dictionaries with defaults."""
        self.acf_pacf_config = Args.acf_pacf.build(columns=[self.target])
        self.categorical_columns_config = Args.categorical_columns.build()
        self.causality_test_config = Args.causality_test.build(target_column=self.target, date_column=self.date_column)
        self.correlation_chart_layout_config = Args.corr_chart_layout.build()
        self.correlation_config = Args.correlation.build()
        self.kpi_vs_feature_config = Args.kpi_vs_feature.build(target_column=self.target, date_column=self.date_column)
        self.outlier_chart_layout_config = Args.outlier.build()
        self.time_aggregator_config = Args.time_aggregator.build(date_column=self.date_column)
        self.time_comparison_chart_config = Args.time_comparison_chart.build(date_column=self.date_column)
        self.time_comparison_config = Args.time_comparison.build(date_column=self.date_column)
        self.time_series_config = Args.time_series.build(columns=self.target)
        self.vif_config = Args.vif.build(target_column=self.target)
        self.distribution_chart_config = Args.distribution_chart.build()

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

    # Deprecated set methods for backward compatibility - these will be removed in future versions

    @deprecated("update_acf_pacf_config")
    def set_acf_pacf_config(self, **kwargs: Unpack[SetAcfPacfConfigArgs]) -> Self:
        pass

    @deprecated("update_categorical_columns_config")
    def set_categorical_columns_config(self, **kwargs: Unpack[SetCategoricalColumnsConfigArgs]) -> Self:
        pass

    @deprecated("update_causality_test_config")
    def set_causality_test_config(self, **kwargs: Unpack[SetCausalityTestConfigArgs]) -> Self:
        pass

    @deprecated("update_correlation_chart_layout_config")
    def set_correlation_chart_layout_config(self, **kwargs: Unpack[SetCorrChartLayoutConfigArgs]) -> Self:
        pass

    @deprecated("update_corr_chart_layout_config")
    def set_corr_chart_layout_config(self, **kwargs: Unpack[SetCorrChartLayoutConfigArgs]) -> Self:
        pass

    @deprecated("update_correlation_config")
    def set_correlation_config(self, **kwargs: Unpack[SetCorrelationConfigArgs]) -> Self:
        pass

    @deprecated("update_distribution_chart_config")
    def set_distribution_chart_config(self, **kwargs: Unpack[SetDistributionChartConfigArgs]) -> Self:
        pass

    @deprecated("update_kpi_vs_feature_config")
    def set_kpi_vs_feature_config(self, **kwargs: Unpack[SetKPIVsFeatureConfigArgs]) -> Self:
        pass

    @deprecated("update_outlier_chart_layout_config")
    def set_outlier_chart_layout_config(self, **kwargs: Unpack[SetOutlierConfigArgs]) -> Self:
        pass

    @deprecated("update_time_aggregator_config")
    def set_time_aggregator_config(self, **kwargs: Unpack[SetTimeAggregatorConfigArgs]) -> Self:
        pass

    @deprecated("update_time_comparison_chart_config")
    def set_time_comparison_chart_config(self, **kwargs: Unpack[SetTimeComparisonChartConfigArgs]) -> Self:
        pass

    @deprecated("update_time_comparison_config")
    def set_time_comparison_config(self, **kwargs: Unpack[SetTimeComparisonConfigArgs]) -> Self:
        pass

    @deprecated("update_time_series_config")
    def set_time_series_config(self, **kwargs: Unpack[SetTimeSeriesConfigArgs]) -> Self:
        pass

    @deprecated("update_vif_config")
    def set_vif_config(self, **kwargs: Unpack[SetVIFConfigArgs]) -> Self:
        pass

    # New update methods with defaults and validation

    def update_acf_pacf_config(self, **kwargs: Unpack[SetAcfPacfConfigArgs]) -> Self:
        self.acf_pacf_config = replace(self.acf_pacf_config, **kwargs)
        return self

    def update_categorical_columns_config(self, **kwargs: Unpack[SetCategoricalColumnsConfigArgs]) -> Self:
        self.categorical_columns_config = replace(self.categorical_columns_config, **kwargs)
        return self
    
    def update_causality_test_config(self, **kwargs: Unpack[SetCausalityTestConfigArgs]) -> Self:
        self.causality_test_config = replace(self.causality_test_config, **kwargs)
        return self

    def update_correlation_chart_layout_config(self, **kwargs: Unpack[SetCorrChartLayoutConfigArgs]) -> Self:
        self.correlation_chart_layout_config = replace(self.correlation_chart_layout_config, **kwargs)
        return self

    def update_corr_chart_layout_config(self, **kwargs: Unpack[SetCorrChartLayoutConfigArgs]) -> Self:
        self.correlation_chart_layout_config = replace(self.correlation_chart_layout_config, **kwargs)
        return self

    def update_correlation_config(self, **kwargs: Unpack[SetCorrelationConfigArgs]) -> Self:
        self.correlation_config = replace(self.correlation_config, **kwargs)
        return self

    def update_distribution_chart_config(self, **kwargs: Unpack[SetDistributionChartConfigArgs]) -> Self:
        self.distribution_chart_config = replace(self.distribution_chart_config, **kwargs)
        return self

    def update_kpi_vs_feature_config(self, **kwargs: Unpack[SetKPIVsFeatureConfigArgs]) -> Self:
        self.kpi_vs_feature_config = replace(self.kpi_vs_feature_config, **kwargs)
        return self

    def update_outlier_chart_layout_config(self, **kwargs: Unpack[SetOutlierConfigArgs]) -> Self:
        self.outlier_chart_layout_config = replace(self.outlier_chart_layout_config, **kwargs)
        return self

    def update_time_aggregator_config(self, **kwargs: Unpack[SetTimeAggregatorConfigArgs]) -> Self:
        self.time_aggregator_config = replace(self.time_aggregator_config, **kwargs)
        return self

    def update_time_comparison_chart_config(self, **kwargs: Unpack[SetTimeComparisonChartConfigArgs]) -> Self:
        self.time_comparison_chart_config = replace(self.time_comparison_chart_config, **kwargs)
        return self

    def update_time_comparison_config(self, **kwargs: Unpack[SetTimeComparisonConfigArgs]) -> Self:
        self.time_comparison_config = replace(self.time_comparison_config, **kwargs)
        return self

    def update_time_series_config(self, **kwargs: Unpack[SetTimeSeriesConfigArgs]) -> Self:
        self.time_series_config = replace(self.time_series_config, **kwargs)
        return self

    def update_vif_config(self, **kwargs: Unpack[SetVIFConfigArgs]) -> Self:
        self.vif_config = replace(self.vif_config, **kwargs)
        return self
