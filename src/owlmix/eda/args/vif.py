from dataclasses import dataclass, field
from typing import TypedDict, NotRequired, Unpack


DEFAULT_COLOR_THRESHOLDS  = [(5, "green"), (10, "orange"), (float("inf"), "red")]


class SetVIFConfigArgs(TypedDict):
    target_column: NotRequired[str]
    features: NotRequired[list[str]]
    precision: NotRequired[int]
    color_thresholds: NotRequired[list[tuple[int, str]]]


@dataclass
class VIF:
    target_column: str | None = None
    features: list[str] | None = None
    precision: int | None = None
    color_thresholds: list[tuple[int, str]] | None = field(default_factory=DEFAULT_COLOR_THRESHOLDS)


def build(**values: Unpack[SetVIFConfigArgs]) -> VIF:
    """
    Build a VIF object from the provided keyword arguments.
    Args:
        target_column: str - name of the target column for VIF calculation
        features: list[str] - list of feature column names to calculate VIF against the target column
        precision: int - number of decimal places to round the VIF values to
    Returns:
        VIF object with the provided configuration
    """
    values = values or {}
    return VIF(
        target_column=values.get("target_column"),
        features=values.get("features"),
        precision=values.get("precision", 3),  # default precision to 3 if not provided
        color_thresholds=values.get("color_thresholds", DEFAULT_COLOR_THRESHOLDS),
    )