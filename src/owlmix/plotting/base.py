import os
from typing import Dict

class BasePlotter:
    """
    Base class for all plotters in the owlmix library.
    Provides common functionality and interface for all plotters.
    """

    def __init__(self, data: Dict, params):
        self.data = data
        self.params = params

    def makedirs(self, path: str):
        """
        Utility method to create directories if they do not exist.

        Args:
            path (str): The directory path to create.
        """
        os.makedirs(path, exist_ok=True)

    def generate(self):
        """
        Abstract method to be implemented by all subclasses.
        Should contain the logic to create the plot.
        """
        raise NotImplementedError("Subclasses must implement the generate method.")