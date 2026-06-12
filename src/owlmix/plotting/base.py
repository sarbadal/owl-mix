import os
from typing import Any

class BasePlotter:
    """
    Base class for all plotters in the owlmix library.
    Provides common functionality and interface for all plotters.
    """

    def __init__(self, data: Any = None, params: Any = None, **_: Any):
        self.data = data
        self.params = params

    def makedirs(self, path: str):
        """
        Utility method to create directories if they do not exist.

        Args:
            path (str): The directory path to create.
        """
        os.makedirs(path, exist_ok=True)

    def generate(self, *args: Any, **kwargs: Any):
        """
        Abstract method to be implemented by all subclasses.
        Should contain the logic to create the plot.
        """
        raise NotImplementedError("Subclasses must implement the generate method.")

    def plot(self, *args: Any, **kwargs: Any):
        """Compatibility wrapper for plotter classes exposing plot()."""
        return self.generate(*args, **kwargs)

    def apply_transformation(self, *args: Any, **kwargs: Any):
        """No-op compatibility hook for transformation-based plotters."""
        return self

    def prepare(self, *args: Any, **kwargs: Any):
        """No-op compatibility hook for preparer-style usage."""
        return self.data

    def generate_chart_for_all(self, *args: Any, **kwargs: Any):
        """Compatibility wrapper when a plotter provides per-series chart generation."""
        return self.generate(*args, **kwargs)