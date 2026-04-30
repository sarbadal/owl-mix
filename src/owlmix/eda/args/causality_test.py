from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetCausalityTestConfigArgs(TypedDict):
    target_column: NotRequired[str]
    columns: NotRequired[list[str]]
    max_lag: NotRequired[int]
    error_threshold: NotRequired[float]


@dataclass
class CausalityTest:
    target_column: str | None = None
    columns: list[str] | None = None
    max_lag: int | None = 5
    error_threshold: float | None = 0.15


def build(**values: Unpack[SetCausalityTestConfigArgs]) -> CausalityTest:
    """
    Build a CausalityTest object from the provided keyword arguments.
    Args:
        target_column: str - name of the target column for causality testing
        columns: list[str] - list of column names to test causality against the target column
        max_lag: int - maximum lag to consider for causality testing
        error_threshold: float - threshold for error in causality testing
    Returns:
        CausalityTest object with the provided configuration
    """    
    values = values or {}
    return CausalityTest(
        target_column=values.get("target_column", None),
        columns=values.get("columns", None),
        max_lag=values.get("max_lag", 5),  # default max_lag to 5 if not provided
        error_threshold=values.get("error_threshold", 0.15) # default error_threshold to 0.15 if not provided
    )