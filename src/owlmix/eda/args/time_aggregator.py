from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetTimeAggregatorConfigArgs(TypedDict):
    date_column: NotRequired[str]
    value_columns: NotRequired[list[str]]
    agg_func: NotRequired[str]
    precision: NotRequired[int]
    freq: NotRequired[str]


@dataclass
class TimeAggregator:
    date_column: str | None = None
    value_columns: list[str] | None = None
    agg_func: str | None = None
    precision: int | None = None
    freq: int | None = None


def build(**values: Unpack[SetTimeAggregatorConfigArgs]) -> TimeAggregator:
    """
    Build a TimeAggregator configuration object from the provided values.
    Args:
        date_column: Optional date column name.
        value_columns: Optional list of value columns.
        agg_func: Optional aggregation function.
        precision: Optional integer for precision.
        freq: Optional integer for frequency.
    Returns:
        TimeAggregator object with the provided configuration.
    """
    values = values or {}
    return TimeAggregator(
        date_column=values.get("date_column", None),
        value_columns=values.get("value_columns", None),
        agg_func=values.get("agg_func", "sum"),  # default aggregation function to 'sum' if not provided
        precision=values.get("precision", 2),  # default precision to 2 if not provided
        freq=values.get("freq", "YE")  # default frequency to 'YE' if not provided
    )
