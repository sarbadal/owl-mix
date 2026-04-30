from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetDistributionChartConfigArgs(TypedDict):
    columns: NotRequired[str]
    max_charts_per_row: NotRequired[int]


@dataclass
class DistributionChart:
    columns: str | None = None
    max_charts_per_row: int | None = 3

def build(**values: Unpack[SetDistributionChartConfigArgs]) -> DistributionChart:
    """
    Build a DistributionChart configuration object from the provided values.
    Args:
        columns: Optional column name to include in the distribution chart analysis.
        max_charts_per_row: Optional integer for max charts per row.
    Returns:
        DistributionChart object with the provided configuration.
    """
    values = values or {}
    return DistributionChart(
        columns=values.get("columns", None),
        max_charts_per_row=values.get("max_charts_per_row", 3) # default to 3 if not provided
    )
