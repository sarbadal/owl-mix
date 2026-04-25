# owlmix/eda/summary_builder_config.py
import pandas as pd
from typing import Self, TypedDict, Unpack, NotRequired, Literal, Callable, Any


class SetCausalityTestConfigArgs(TypedDict):
    target_column: NotRequired[str]
    columns: NotRequired[list[str]]
    max_lag: NotRequired[int]
    error_threshold: NotRequired[float]


class SetVIFConfigArgs(TypedDict):
    target_column: NotRequired[str]
    features: NotRequired[list[str]]
    precision: NotRequired[int]

Period = Literal["daily", "weekly", "monthly", "yearly"]

class SetKPIVsFeatureConfigArgs(TypedDict):
    target_column: NotRequired[str]
    columns: NotRequired[list[str]]
    period: NotRequired[Period]
    date_column: NotRequired[str]
    agg_func: NotRequired[str]


class SetAcfPacfConfigArgs(TypedDict):
    columns: NotRequired[list[str]]
    n_lags: NotRequired[int]


class SetCorrelationConfigArgs(TypedDict):
    columns: NotRequired[list[str]]


ComparisonType = Literal["yoy", "mom", "wow"]

class SetTimeComparisonConfigArgs(TypedDict):
    date_column: NotRequired[str]
    value_columns: NotRequired[list[str]]
    comparison_type: NotRequired[ComparisonType]
    agg_func: NotRequired[str]
    precision: NotRequired[int]
    freq: NotRequired[str]


class SetTimeAggregatorConfigArgs(TypedDict):
    date_column: NotRequired[str]
    value_columns: NotRequired[list[str]]
    agg_func: NotRequired[str]
    precision: NotRequired[int]
    freq: NotRequired[int]


class SetOutlierConfigArgs(TypedDict):
    columns: NotRequired[list[str]]
    max_cols_per_chart: NotRequired[int]
    single_image: NotRequired[bool]


class SetCorrChartLayoutConfigArgs(TypedDict):
    columns: NotRequired[list[str]]
    precision: NotRequired[int]


class SetCategoricalColumnsConfigArgs(TypedDict):
    columns: NotRequired[list[str]]


class SummaryBuilderConfig:

    def __init__(self, df: pd.DataFrame, target: str, date_column: str):
        self.df = df
        self.target = target
        self.date_column = date_column
        self.init_config()

    def init_config(self) -> None:
        """Initialize all configuration dictionaries with defaults."""
        self.outlier_chart_layout_config = {
            "columns": None,
            "max_cols_per_chart": 4,
            "single_image": True
        }

        self.correlation_chart_layout_config = {
            "columns": None,
            "precision": 2
        }

        self.correlation_config = {
            "columns": None
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

        self.categorical_columns_config = {
            "columns": None
        }

        self.kpi_vs_feature_config = {
            "target_column": self.target,
            "columns": None,
            "period": "weekly",
            "date_column": self.date_column,
            "agg_func": "sum"
        }

        self.causality_test_config = {
            "target_column": self.target,
            "columns": None,
            "max_lag": 5,
            "error_threshold": 0.15
        }

        self.time_comparison_config = {
            "date_column": self.date_column,
            "value_columns": None,
            "comparison": "yoy",
            "agg_func": "sum",
            "precision": 2,
            "freq": "ME"
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
        """
        Set Causality Test configuration.

        Args:
            target_column: str - target column name
            columns: list[str] - columns to test
            max_lag: int - maximum lag for testing
            error_threshold: float - error threshold for MAPE
        """
        max_lag = kwargs.get("max_lag")
        self._validate_positive_int(max_lag, "max_lag")

        updates = {
            "target_column": kwargs.get("target_column", self.causality_test_config["target_column"]),
            "columns": kwargs.get("columns"),
            "max_lag": max_lag or self.causality_test_config["max_lag"],
            "error_threshold": kwargs.get("error_threshold") or self.causality_test_config["error_threshold"]
        }
        self._update_config(self.causality_test_config, updates)
        return self

    def set_vif_config(self, **kwargs: Unpack[SetVIFConfigArgs]) -> Self:
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

    def set_kpi_vs_feature_config(self, **kwargs: Unpack[SetKPIVsFeatureConfigArgs]) -> Self:
        """
        Set KPI vs Feature configuration.

        Args:
            target_column: str - target column name
            columns: list[str] - feature columns
            period: str - it could be any of "daily", "weekly", "monthly", "yearly"
            date_column: str - date column name
            agg_func: str - aggregation function (sum, mean, etc.)
        """
        updates = {
            "target_column": kwargs.get("target_column") or self.target,
            "columns": kwargs.get("columns"),
            "period": kwargs.get("period") or "weekly",
            "date_column": kwargs.get("date_column") or self.date_column,
            "agg_func": kwargs.get("agg_func") or "sum"
        }
        self._update_config(self.kpi_vs_feature_config, updates)
        return self

    def set_acf_pacf_config(self, **kwargs: Unpack[SetAcfPacfConfigArgs]) -> Self:
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

    def set_correlation_config(self, **kwargs: Unpack[SetCorrelationConfigArgs]) -> Self:
        """
        Set Correlation configuration.

        Args:
            columns: list[str] - columns for correlation analysis
        """
        updates = {"columns": kwargs.get("columns")}
        self._update_config(self.correlation_config, updates)
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
        """
        Set Correlation Chart Layout configuration.

        Args:
            columns: list[str] - columns for analysis
            precision: int - decimal precision
        """
        precision = kwargs.get("precision", 2)
        self._validate_positive_int(precision, "precision")

        updates = {
            "columns": kwargs.get("columns"),
            "precision": precision
        }
        self._update_config(self.correlation_chart_layout_config, updates)
        return self

    def set_categorical_columns_config(self, **kwargs: Unpack[SetCategoricalColumnsConfigArgs]) -> Self:
        """
        Set Categorical Columns configuration.

        Args:
            columns: list[str] - categorical columns
        """
        updates = {"columns": kwargs.get("columns")}
        self._update_config(self.categorical_columns_config, updates)
        return self