from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetTimeSeriesConfigArgs(TypedDict):
    columns: NotRequired[str]
    model: NotRequired[str]
    period: NotRequired[int] | None = None


@dataclass
class TimeSeries:
    columns: str | None = None
    model: str = "additive"
    period: int | None = None


def build(**values: Unpack[SetTimeSeriesConfigArgs]) -> TimeSeries:
    """
    Build a TimeSeries configuration object from the provided values.
    Args:
        columns: Optional column name to include in the time series analysis.
        model: Optional model type for the time series analysis.
            "additive" (default) or "multiplicative".
    Returns:
        TimeSeries object with the provided configuration.
    """
    values = values or {}
    return TimeSeries(
        columns=values.get("columns", None),
        model=values.get("model", "additive"),
        period=values.get("period", None),
    )
