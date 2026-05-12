from typing import Dict

class BaseAnalyzer:
    """
    Base class for all analyzers in the owlmix library.
    Provides common functionality and interface for all analyzers.
    """

    def __init__(self, df, params):
        self.df = df.copy()
        self.params = params

    def compute(self):
        """
        Abstract method to be implemented by all subclasses.
        Should contain the logic to perform the analysis.
        """
        raise NotImplementedError("Subclasses must implement the compute method.")