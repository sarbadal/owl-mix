from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack
from owlmix.typing.types import ComparisonType, PlotModeType


class SetTimeComparisonChartConfigArgs(TypedDict):
    date_column: NotRequired[str]
    value_columns: NotRequired[list[str]]
    comparison_type: NotRequired[ComparisonType]
    agg_func: NotRequired[str]
    mode: NotRequired[PlotModeType]


@dataclass
class TimeComparisonChart:
    date_column: str | None = None
    value_columns: list[str] | None = None
    comparison_type: ComparisonType | None = None
    agg_func: str | None = None
    mode: PlotModeType | None = None


def build(**values: Unpack[SetTimeComparisonChartConfigArgs]) -> TimeComparisonChart:
    """
    Build a TimeComparisonChart configuration object from the provided values.
    Args:
        date_column: Optional date column name.
        value_columns: Optional list of value columns.
        comparison_type: Optional comparison type.
        agg_func: Optional aggregation function.
        mode: Optional plot mode type.
    Returns:
        TimeComparisonChart object with the provided configuration.
    """
    values = values or {}
    return TimeComparisonChart(
        date_column=values.get("date_column", None),
        value_columns=values.get("value_columns", None),
        comparison_type=values.get("comparison_type", "yoy"),  # default comparison type to 'yoy' if not provided
        agg_func=values.get("agg_func", "sum"),  # default aggregation function to 'sum' if not provided
        mode=values.get("mode", "pct_change")  # default mode to 'pct_change' if not provided
    )
