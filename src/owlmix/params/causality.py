from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class CausalityConfigArgs(TypedDict):
    """Configuration parameters for Causality analysis."""
    target_column: NotRequired[str]
    columns: NotRequired[list[str]]
    max_lag: NotRequired[int]
    error_threshold: NotRequired[float]
    p_value_weight: NotRequired[float]
    mape_weight: NotRequired[float]
    precision: NotRequired[int]


@dataclass
class Causality:
    """Configuration parameters for Causality analysis."""
    target_column: str | None = None
    columns: list[str] | None = None
    max_lag: int = 5
    error_threshold: float = 0.15
    p_value_weight: float = 0.6
    mape_weight: float = 0.4
    precision: int = 3


def build(**values: Unpack[CausalityConfigArgs]) -> Causality:
    """
    Build a Causality configuration object from the provided values.
    Args:
        target_column: name of the target column for causality analysis
        columns: list of column names to include in the causality analysis
        max_lag: maximum lag to test for causality
        error_threshold: MAPE threshold for determining causality
        p_value_weight: weight for p-value in combined score calculation
        mape_weight: weight for MAPE in combined score calculation
        precision: number of decimal places to round results
    Returns:
        Causality object with the provided configuration
    """
    values = values or {}
    return Causality(**values)