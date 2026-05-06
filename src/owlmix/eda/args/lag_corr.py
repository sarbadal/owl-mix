from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetLagCorrelationChartArgs(TypedDict):
    column: str
    lag: NotRequired[int]


@dataclass
class LagCorrelation:
    column: str
    lag: int = 2


def build(**values: Unpack[SetLagCorrelationChartArgs]) -> LagCorrelation:
    """
    Build a LagCorrelation configuration object from the provided values.
    Args:
        column: The name of the column to analyze for lag correlation.
        lag: The number of periods to lag (default is 2).
    Returns:
        LagCorrelation object with the provided configuration.
    """
    values = values or {}
    return LagCorrelation(
        column=values.get("column"),
        lag=values.get("lag", 2)  # default to 2 if not provided
    )