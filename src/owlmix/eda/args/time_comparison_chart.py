from dataclasses import dataclass
from typing import TypedDict, NotRequired
from owlmix.typing.types import ComparisonType, PlotModeType

class SetTimeComparisonChartConfigArgs(TypedDict):
    date_column: NotRequired[str]
    value_columns: NotRequired[list[str]]
    comparison_type: NotRequired[ComparisonType]
    agg_func: NotRequired[str]
    mode: NotRequired[PlotModeType]

@dataclass
class TimeComparisonChartConfigArgs:
    date_column: str | None = None
    value_columns: list[str] | None = None
    comparison_type: ComparisonType | None = None
    agg_func: str | None = None
    mode: PlotModeType | None = None

def build(data: TimeComparisonChartConfigArgs) -> SetTimeComparisonChartConfigArgs:
    return {
        "date_column": data.date_column,
        "value_columns": data.value_columns,
        "comparison_type": data.comparison_type,
        "agg_func": data.agg_func,
        "mode": data.mode
    }
