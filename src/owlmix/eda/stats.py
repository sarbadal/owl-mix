# owlmix/eda/stats.py
import json 
import pandas as pd

from .utils import to_json


class BasicStats:
    """Computes basic statistical summaries for a pandas DataFrame."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the BasicStats object.

        Args:
            df (pd.DataFrame): The DataFrame to analyze.
        """
        self.df = df
        self.result = None

    def compute(self) -> dict:
        """
        Compute descriptive statistics for the DataFrame.

        Returns:
            dict: A dictionary containing the summary statistics.
        """
        description = self.df.describe(include="all")
        self.result = {
            "summary": description.fillna("").to_dict()
        }
        return self.result

    def to_json(self) -> str:
        """
        Serialize the computed statistics to a JSON string.

        Returns:
            str: The summary statistics in JSON format.
        """
        if self.result is None:
            self.compute()
        return to_json(self.result)