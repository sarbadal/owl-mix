from dataclasses import dataclass, field
from typing import Callable, TypedDict, NotRequired, Unpack


class DistNumericConfigArgs(TypedDict):
    """Configuration parameters for Distribution of Numerical Columns section."""
    columns: NotRequired[list[str]]
    show_normal_curve: NotRequired[bool]
    dpi: NotRequired[int]
    figsize: NotRequired[tuple[float, float]]
    filename_prefix: NotRequired[str]


@dataclass
class DistNumeric:
    """Configuration parameters for Distribution of Numerical Columns section."""
    columns: list[str] = field(default_factory=list)
    show_normal_curve: bool = True
    dpi: int = 150
    figsize: tuple[float, float] = (6.0, 4.0)
    filename_prefix: str = "distribution"


def build(**values: Unpack[DistNumericConfigArgs]) -> DistNumeric:
    """
    Build a DistNumeric configuration object from the provided values.
    Args:
        columns: list of column names to generate distribution plots for
        show_normal_curve: whether to overlay a normal distribution curve on the histogram
        dpi: resolution of the output images
        figsize: size of the output images in inches (width, height)
        filename_prefix: prefix for the generated image filenames
    Returns:
        DistNumeric: The configuration object with the provided values.
    """
    values = values or {}
    return DistNumeric(**values)