from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class CorrelationConfigArgs(TypedDict):
    """Configuration parameters for Correlation analysis."""
    columns: NotRequired[list[str]]
    n_lags: NotRequired[int]
    precision: NotRequired[int]


@dataclass
class Correlation:
    """Configuration parameters for Correlation analysis."""
    columns: list[str] | None = None
    n_lags: int | None = 5
    precision: int = 3


def build(**values: Unpack[CorrelationConfigArgs]) -> Correlation:
    """
    Build a Correlation configuration object from the provided values.
    Args:
        columns: list of column names to include in the correlation analysis
        n_lags: number of lags to compute for lagged correlation
        precision: number of decimal places to round correlation values
    Returns:
        Correlation object with the provided configuration
    """
    values = values or {}
    return Correlation(**values)
