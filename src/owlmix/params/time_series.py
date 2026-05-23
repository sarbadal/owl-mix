from dataclasses import dataclass, field
from typing import Callable, TypedDict, NotRequired, Unpack


class TimeSeriesPlotConfigArgs(TypedDict):
    """Configuration parameters for Time Series Plotting."""
    date_column: NotRequired[str]
    target_column: NotRequired[str]
    period: NotRequired[int]
    model: NotRequired[str]
    dpi: NotRequired[int]
    figsize: NotRequired[tuple[float, float]]
    filename_prefix: NotRequired[str]


@dataclass
class TimeSeriesPlot:
    """Configuration parameters for Time Series Plotting."""
    date_column: str = ""
    target_column: str = ""
    period: int = 12
    model: str = "additive"  # "additive" or "multiplicative"
    dpi: int = 150
    figsize: tuple[float, float] = (24.0, 4.0)
    filename_prefix: str = "time_series_decomposition"


def build(**values: Unpack[TimeSeriesPlotConfigArgs]) -> TimeSeriesPlot:
    """
    Build a TimeSeriesPlot configuration object from the provided values.
    Args:
        date_column: name of the date column in the DataFrame
        target_column: name of the target (value) column in the DataFrame
        period: seasonality period (e.g., 12 for monthly data with yearly seasonality)
        model: type of decomposition model ("additive" or "multiplicative")
        dpi: resolution of the output images
        figsize: size of the output images in inches (width, height)
        filename_prefix: prefix for the generated image filenames
    Returns:
        TimeSeriesPlot: A configured TimeSeriesPlot object.
    """
    values = values or {}
    return TimeSeriesPlot(**values)