from dataclasses import dataclass, field
from typing import Callable, TypedDict, NotRequired, Unpack

from ..mmm.models.base import BaseModel
from ..mmm.models.sklearn import SimpleLinearModelSK
from ..mmm.pipeline.pipeline import TransformerPipeline


class ResponseCurveConfigArgs(TypedDict):
    """Configuration parameters for Response Curve analysis."""
    model: NotRequired[BaseModel]
    curve_type: NotRequired[str]
    transformers: NotRequired[dict[str, TransformerPipeline]]
    feature_columns: NotRequired[list[str]]
    target_column: NotRequired[str]
    add_default_transformers: NotRequired[bool]
    line_color: NotRequired[str]
    fitted_line_color: NotRequired[str]
    label_color: NotRequired[str]


@dataclass
class ResponseCurve:
    """Configuration parameters for Response Curve analysis."""
    model: BaseModel = None
    curve_type: str = "exponential"
    transformers: dict[str, TransformerPipeline] | None = None
    feature_columns: list[str] = field(default_factory=list)
    target_column: str = None
    add_default_transformers: bool = True
    line_color: str = "#1f77b4"  # blue
    fitted_line_color: str = "#ff7f0e"  # orange
    label_color: str = "#888888"  # neutral gray


def build(**values: Unpack[ResponseCurveConfigArgs]) -> ResponseCurve:
    """
    Build a ResponseCurve configuration object from the provided values.
    Args:
        model: instance of the response curve model to use
        transformers: dictionary of feature transformers to apply
        feature_columns: list of column names to use as features in the model
        target_column: name of the column to use as the target variable
    Returns:
        ResponseCurve object with the provided configuration
    """
    values = values or {}
    return ResponseCurve(**values)