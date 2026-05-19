from dataclasses import dataclass
from typing import Callable, TypedDict, NotRequired, Unpack


class ResponseCurveConfigArgs(TypedDict):
    """Configuration parameters for Response Curve analysis."""
    model_type: NotRequired[str]
    feature_columns: NotRequired[list[str]]
    target_column: NotRequired[str]
    time_column: NotRequired[str]
    transformations: NotRequired[dict[str, Callable]]
    baseline: NotRequired[str]


@dataclass
class ResponseCurve:
    """Configuration parameters for Response Curve analysis."""
    model_type: str = "linear"
    feature_columns: list[str] | None = None
    target_column: str | None = None
    time_column: str | None = None
    transformations: dict[str, Callable] | None = None
    baseline: str | None = None


def build(**values: Unpack[ResponseCurveConfigArgs]) -> ResponseCurve:
    """
    Build a ResponseCurve configuration object from the provided values.
    Args:
        model_type: type of response curve model to use (e.g., "linear", "nonlinear")
        feature_columns: list of column names to use as features in the model
        target_column: name of the column to use as the target variable
        time_column: name of the column representing time (if applicable)
        transformations: dictionary of transformations to apply to features (e.g., {"feature1": log_transform})
        baseline: name of the baseline scenario for comparison (if applicable)
    Returns:
        ResponseCurve object with the provided configuration
    """
    values = values or {}
    return ResponseCurve(**values)