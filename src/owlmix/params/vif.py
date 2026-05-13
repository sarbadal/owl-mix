from dataclasses import dataclass, field
from typing import TypedDict, NotRequired, Unpack

DEFAULT_COLOR_THRESHOLDS  = [(5, "green"), (10, "orange"), (float("inf"), "red")]

class VifConfigArgs(TypedDict):
    target_column: NotRequired[str]
    features: NotRequired[list[str]]
    precision: NotRequired[int]
    color_thresholds: NotRequired[list[tuple[int, str]]]


@dataclass
class Vif:
    target_column: str | None = None
    features: list[str] | None = None
    precision: int | None = 3
    color_thresholds: list[tuple[int, str]] | None = field(default_factory=lambda: DEFAULT_COLOR_THRESHOLDS.copy())


def build(**values: Unpack[VifConfigArgs]) -> Vif:
    """
    Build a Vif object from the provided keyword arguments.
    Args:
        target_column: str - name of the target column for VIF calculation
        features: list[str] - list of feature column names to calculate VIF against the target column
        precision: int - number of decimal places to round the VIF values to
    Returns:
        Vif object with the provided configuration
    """
    values = values or {}
    return Vif(**values)