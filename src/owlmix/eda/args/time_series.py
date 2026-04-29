from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetTimeSeriesConfigArgs(TypedDict):
    columns: NotRequired[str]


@dataclass
class TimeSeries:
    columns: str | None = None


def build(**values: Unpack[SetTimeSeriesConfigArgs]) -> TimeSeries:
    """
    Build a TimeSeries configuration object from the provided values.
    Args:
        columns: Optional column name to include in the time series analysis.
    Returns:
        TimeSeries object with the provided configuration.
    """
    values = values or {}
    return TimeSeries(
        columns=values.get("columns", None)
    )
