from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class BoxPlotConfigArgs(TypedDict):
    """Configuration parameters for box plot generation."""
    columns: NotRequired[list[str]]
    method: NotRequired[str]
    threshold: NotRequired[float]
    precision: NotRequired[int]
    n_plot_per_row: NotRequired[int]


@dataclass
class BoxPlot:
    """Configuration parameters for box plot generation."""
    columns: list[str] | None = None
    method: str = 'iqr'
    threshold: float | None = None
    precision: int = 2
    n_plot_per_row: int = 4

    def __post_init__(self):
        if self.method not in ['iqr', 'zscore']:
            raise ValueError(f"Unsupported method: {self.method}. Supported methods are 'iqr' and 'zscore'.")
        if self.precision < 0:
            raise ValueError("Precision must be a non-negative integer.")
        # if self.threshold is None:
        #     self.threshold = 1.5 if self.method == 'iqr' else 3.0


def build(**values: Unpack[BoxPlotConfigArgs]) -> BoxPlot:
    """
    Build a BoxPlot configuration object from the provided values.
    Args:
        n_plot_per_row: number of box plots to display per row in the grid layout
    Returns:
        BoxPlot object with the provided configuration
    """
    values = values or {}
    return BoxPlot(**values)