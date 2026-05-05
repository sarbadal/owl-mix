from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetCausalityTestConfigArgs(TypedDict):
    target_column: NotRequired[str]
    columns: NotRequired[list[str]]
    max_lag: NotRequired[int]
    error_threshold: NotRequired[float]
    p_value_weight: NotRequired[float]
    mape_weight: NotRequired[float]


@dataclass
class CausalityTest:
    target_column: str | None = None
    columns: list[str] | None = None
    max_lag: int | None = 5
    error_threshold: float | None = 0.15
    p_value_weight: float | None = None
    mape_weight: float | None = None

    def validate_weights(self):
        p = self.p_value_weight
        m = self.mape_weight

        # Both provided
        if p is not None and m is not None:
            if not (0 <= p <= 1 and 0 <= m <= 1):
                raise ValueError("p_value_weight and mape_weight must be between 0 and 1.")
            if abs(p + m - 1) > 1e-8:
                raise ValueError("p_value_weight and mape_weight must sum to 1.")
            return self

        # Only p_value_weight provided
        if p is not None:
            if not (0 <= p <= 1):
                raise ValueError("p_value_weight must be between 0 and 1.")
            self.mape_weight = 1 - p
            return self

        # Only mape_weight provided
        if m is not None:
            if not (0 <= m <= 1):
                raise ValueError("mape_weight must be between 0 and 1.")
            self.p_value_weight = 1 - m
            return self

        # Neither provided, set defaults
        self.p_value_weight = 0.4
        self.mape_weight = 0.6

        return self


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
        error_threshold=values.get("error_threshold", 0.15), # default error_threshold to 0.15 if not provided
    )