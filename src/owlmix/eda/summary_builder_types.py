from dataclasses import dataclass
from typing import TypedDict, NotRequired


@dataclass
class CausalityTestConfigArgs:
    target_column: str | None = None
    columns: list[str] | None = None
    max_lag: int | None = None
    error_threshold: float | None = None


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
    period: NotRequired[PeriodType]
    date_column: NotRequired[str]
    agg_func: NotRequired[str]


class SetAcfPacfConfigArgs(TypedDict):
    columns: NotRequired[list[str]]
    n_lags: NotRequired[int]


class SetCorrelationConfigArgs(TypedDict):
    columns: NotRequired[list[str]]


class SetTimeComparisonConfigArgs(TypedDict):
    date_column: NotRequired[str]
    value_columns: NotRequired[list[str]]
    comparison_type: NotRequired[ComparisonType]
    agg_func: NotRequired[str]
    precision: NotRequired[int]
    freq: NotRequired[str]


class SetTimeComparisonChartConfigArgs(TypedDict):
    date_column: NotRequired[str]
    value_columns: NotRequired[list[str]]
    comparison_type: NotRequired[ComparisonType]
    agg_func: NotRequired[str]
    mode: NotRequired[PlotModeType]


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