from typing import Any

class BaseAnalyzer:
    """
    Base class for all analyzers in the owlmix library.
    Provides common functionality and interface for all analyzers.
    """

    def __init__(self, df: Any = None, params: Any = None, **_: Any):
        self.df = df.copy(deep=True) if hasattr(df, "copy") else df
        self.params = params
        self.feature_columns: list[str] = []

    def compute(self):
        """
        Abstract method to be implemented by all subclasses.
        Should contain the logic to perform the analysis.
        """
        raise NotImplementedError("Subclasses must implement the compute method.")

    def generate(self, *args: Any, **kwargs: Any):
        """Compatibility wrapper for analyzers used via generate()."""
        return self.compute()

    def set_default_threshold(self) -> None:
        """Optional hook used by analyzers that support threshold defaults."""
        return None