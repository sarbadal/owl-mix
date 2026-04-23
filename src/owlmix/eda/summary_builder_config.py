# owlmix/eda/summary_builder_config.py
import pandas as pd
from typing import Self, TypedDict, NotRequired

from scipy.constants import precision


class SetCausalityTestConfigArgs(TypedDict):
    target_column: NotRequired[str]
    columns: NotRequired[list[str]]
    max_lag: NotRequired[int]
    error_threshold: NotRequired[float]


class SetVIFConfigArgs(TypedDict):
    target_column: NotRequired[str]
    features: NotRequired[list[str]]
    precision: NotRequired[int]


class SetKPIVsFeatureConfigArgs(TypedDict):
    target_column: NotRequired[str]
    columns: NotRequired[list[str]]
    date_column: NotRequired[str]
    date_format: NotRequired[str]
    agg_func: NotRequired[str]


class SetAcfPacfConfigArgs(TypedDict):
    columns: NotRequired[list[str]]
    n_lags: NotRequired[int]


class SetCorrelationConfigArgs(TypedDict):
    columns: NotRequired[list[str]]


class SetTimeComparisonConfigArgs(TypedDict):
    date_column: NotRequired[str]
    value_columns: NotRequired[list[str]]
    comparison_type: NotRequired[str]
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
        """Initialize the configs."""

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
            "date_format": "%Y-%m-%d",
            "date_column": self.date_column,
            "agg_func": "sum",
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
            "columns": self.target,
        }

    def set_causality_test_config(self, **kwargs: SetCausalityTestConfigArgs) -> Self:
        """
        Availability kwargs ...
        kwargs:
            target_column: str = None
            columns: list[str] = None
            max_lag: int = None
            error_threshold: float = None

        Returns: Self
        """
        target_column = kwargs.get("target_column", None)
        columns = kwargs.get("columns", None)
        max_lag = kwargs.get("max_lag", None)
        error_threshold = kwargs.get("error_threshold", None)

        if not isinstance(max_lag, int) or max_lag < 1:
            raise ValueError("max_lag must be a positive integer")

        self.causality_test_config["target_column"] = target_column or self.causality_test_config["target_column"]
        self.causality_test_config["columns"] = columns
        self.causality_test_config["max_lag"] = max_lag or self.causality_test_config["max_lag"]
        self.causality_test_config["error_threshold"] = error_threshold or self.causality_test_config["error_threshold"]

        return self

    def set_vif_config(self, **kwargs: SetVIFConfigArgs) -> Self:
        """
        Availability kwargs ...
        Args:
            target_column: str = None
            features: list[str] = None
            precision: int = 3

        Returns: Self
        """
        target_column = kwargs.get("target_column", None)
        features = kwargs.get("features", None)
        precision = kwargs.get("precision", 3)

        if not isinstance(precision, int) or precision < 1:
            raise ValueError("precision must be a positive integer")

        self.vif_config["target_column"] = target_column
        self.vif_config["features"] = features
        self.vif_config["precision"] = precision

        return self

    def set_kpi_vs_feature_config(self, **kwargs: SetKPIVsFeatureConfigArgs) -> Self:
        """
        Availability kwargs ...
        Args:
            target_column: str = None
            columns: list[str] = None
            date_column: str = None
            date_format: str = "%Y-%m-%d
            agg_func: str = "sum

        Returns: Self
        """
        target_column = kwargs.get("target_column", None)
        columns = kwargs.get("columns", None)
        date_column = kwargs.get("date_column", None)
        date_format = kwargs.get("date_format", "%Y-%m-%d")
        agg_func = kwargs.get("agg_func", "sum")

        self.kpi_vs_feature_config["target_column"] = target_column or self.target
        self.kpi_vs_feature_config["date_format"] = date_format or "%Y-%m-%d"
        self.kpi_vs_feature_config["date_column"] = date_column or self.date_column
        self.kpi_vs_feature_config["agg_func"] = agg_func or "sum"
        self.kpi_vs_feature_config["columns"] = columns

        return self

    def set_acf_pacf_config(self, **kwargs: SetAcfPacfConfigArgs) -> Self:
        """
        Availability kwargs ...
        Args:
            columns: list[str] = None
            n_lags: int = 15

        Returns: Self
        """
        columns = kwargs.get("columns", None)
        n_lags = kwargs.get("n_lags", 15)

        self.acf_pacf_config["columns"] = columns or [self.target]
        self.acf_pacf_config["n_lags"] = n_lags

        return self

    def set_correlation_config(self, **kwargs: SetCorrelationConfigArgs) -> Self:
        """
        Availability kwargs ...
        Args:
            columns: list[str] = None

        Returns: Self
        """
        columns = kwargs.get("columns", None)
        self.correlation_config["columns"] = columns

        return self

    def set_time_series_config(self, **kwargs) -> Self:
        """
        Availability kwargs ...
        Args:
            columns: list[str] = None

        Returns: Self
        """
        columns = kwargs.get("columns", None)

        self.time_series_config["columns"] = columns

        return self

    def set_time_comparison_config(self, **kwargs: SetTimeComparisonConfigArgs) -> Self:
        """
        Availability kwargs ...
        Args:
            date_column: str = None,
            value_columns: list[str] = None,
            comparison_type: str = "yoy",
            agg_func: str = "sum",
            precision: int = 2,
            freq: str = "YE",

        Returns: Self
        """
        date_column = kwargs.get("date_column", None)
        value_columns = kwargs.get("value_columns", None)
        comparison_type = kwargs.get("comparison_type", "yoy")
        agg_func = kwargs.get("agg_func", "sum")
        precision = kwargs.get("precision", 2)

        self.time_comparison_config["date_column"] = date_column if date_column else self.date_column
        self.time_comparison_config["value_columns"] = value_columns
        self.time_comparison_config["comparison_type"] = comparison_type
        self.time_comparison_config["agg_func"] = agg_func
        self.time_comparison_config["precision"] = precision

        self.is_precision_valid(precision)

        return self

    def set_time_aggregator_config(self, **kwargs: SetTimeAggregatorConfigArgs) -> Self:
        """
        Availability kwargs ...
        Args:
            date_column: str = None,
            value_columns: list[str] = None,
            freq: str = "YE",
            agg_func: str = "sum",
            precision: int = 2

        Returns: Self
        """
        date_column = kwargs.get("date_column", None)
        value_columns = kwargs.get("value_columns", None)
        freq = kwargs.get("freq", "YE")
        agg_func = kwargs.get("agg_func", "sum")
        precision = kwargs.get("precision", 2)

        self.time_aggregator_config["date_column"] = date_column or self.date_column
        self.time_aggregator_config["value_columns"] = value_columns
        self.time_aggregator_config["agg_func"] = agg_func
        self.time_aggregator_config["precision"] = precision
        self.time_aggregator_config["freq"] = freq

        self.is_precision_valid(precision)

        return self

    def set_outlier_chart_layout_config(self, **kwargs: SetOutlierConfigArgs) -> Self:
        """
        Availability kwargs ...
        Args:
            columns: list[str] = None,
            max_cols_per_chart: int = 4,
            single_image: bool = True

        Returns: Self
        """
        columns = kwargs.get("columns", None)
        max_cols_per_chart = kwargs.get("max_cols_per_chart", 4)
        single_image = kwargs.get("single_image", True)

        if not isinstance(max_cols_per_chart, int) or max_cols_per_chart < 1:
            raise ValueError("max_cols_per_chart must be a positive integer")

        self.outlier_chart_layout_config["max_cols_per_chart"] = max_cols_per_chart
        self.outlier_chart_layout_config["single_image"] = single_image
        self.outlier_chart_layout_config["columns"] = columns

        return self

    def set_correlation_chart_layout_config(self, **kwargs: SetCorrChartLayoutConfigArgs) -> Self:
        """
        Availability kwargs ...
        Args:
            columns: list[str] = None,
            precision: int = 2

        Returns: Self
        """
        columns = kwargs.get("columns", None)
        precision = kwargs.get("precision", 2)

        self.correlation_chart_layout_config["columns"] = columns
        self.correlation_chart_layout_config["precision"] = precision

        self.is_precision_valid(precision)

        return self

    def set_categorical_columns_config(self, **kwargs: SetCategoricalColumnsConfigArgs) -> Self:
        """
        Availability kwargs ...
        Args:
            columns: list[str] = None

        Returns: Self
        """
        columns = kwargs.get("columns", None)

        self.categorical_columns_config["columns"] = columns

        return self

    def is_precision_valid(self, precision: int) -> None:
        if not isinstance(precision, int) or precision < 1:
            raise ValueError("precision must be a positive integer")