from dataclasses import dataclass
from typing import TypedDict, NotRequired


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


def build(data: TimeComparison) -> SetTimeComparisonConfigArgs:
    return {
        "date_column": data.date_column,
        "value_columns": data.value_columns,
        "comparison_type": data.comparison_type,
        "agg_func": data.agg_func,
        "precision": data.precision,
        "freq": data.freq
    }