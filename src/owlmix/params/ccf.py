from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class CCFConfigArgs(TypedDict):
    """Configuration parameters for Cross-Correlation Function (CCF) analysis."""
    time_column: NotRequired[str]
    target_column: NotRequired[str]
    feature_columns: NotRequired[list[str]]
    max_lag: NotRequired[int]


@dataclass
class CCF:
    """Configuration parameters for Cross-Correlation Function (CCF) analysis."""
    time_column: str | None = None
    target_column: str | None = None
    feature_columns: list[str] | None = None
    max_lag: int = 5


def build(**values: Unpack[CCFConfigArgs]) -> CCF:
    """
    Build a CCF configuration object from the provided values.
    Args:
        time_column: name of the time column in the DataFrame
        target_column: name of the target column for CCF analysis
        feature_columns: list of column names to include as features in the CCF analysis
        max_lag: maximum lag to compute for the CCF analysis
    Returns:
        CCF: A CCF configuration object with the provided values.
    """
    values = values or {}
    return CCF(**values)