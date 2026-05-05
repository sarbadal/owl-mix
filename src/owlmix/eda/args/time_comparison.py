from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack
from ...typing.types import ComparisonType


class SetTimeComparisonConfigArgs(TypedDict):
    date_column: NotRequired[str]
    value_columns: NotRequired[list[str]]
    comparison_type: NotRequired[ComparisonType]
    agg_func: NotRequired[str]
    precision: NotRequired[int]
    freq: NotRequired[str]


@dataclass
class TimeComparison:
    date_column: str | None = None
    value_columns: list[str] | None = None
    comparison_type: ComparisonType | None = None
    agg_func: str | None = None
    precision: int | None = None
    freq: str | None = None


def build(**values: Unpack[SetTimeComparisonConfigArgs]) -> TimeComparison:
    """
    Build a TimeComparison configuration object from the provided values.
    Args:
        date_column: Optional date column name.
        value_columns: Optional list of value columns.
        comparison_type: Optional comparison type.
        agg_func: Optional aggregation function.
        precision: Optional integer for precision.
        freq: Optional string for frequency.
    Returns:
        TimeComparison object with the provided configuration.
    """
    values = values or {}
    return TimeComparison(
        date_column=values.get("date_column", None),
        value_columns=values.get("value_columns", None),
        comparison_type=values.get("comparison_type", "yoy"),
        agg_func=values.get("agg_func", "sum"),  # default aggregation function to 'sum' if not provided
        precision=values.get("precision", 2),  # default precision to 2 if not provided
        freq=values.get("freq", "MED")  # default frequency to 'MED' if not provided
    )