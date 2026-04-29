from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetCorrChartLayoutConfigArgs(TypedDict):
    columns: NotRequired[list[str]]
    precision: NotRequired[int]


@dataclass
class CorrChartLayout:
    columns: list[str] | None = None
    precision: int | None = None


def build(**values: Unpack[SetCorrChartLayoutConfigArgs]) -> CorrChartLayout:
    """
    Build a CorrChartLayout instance from the given values.
    Args:
        columns: Optional list of column names to include in the correlation chart.
        precision: Optional integer specifying the number of decimal places to display in the correlation values.
    Returns:
        CorrChartLayout: The constructed CorrChartLayout instance.
    """
    values = values or {}
    return CorrChartLayout(
        columns=values.get("columns"),
        precision=values.get("precision", 3)  # default precision to 2 if not provided
    )
