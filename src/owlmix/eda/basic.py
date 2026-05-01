# src/owlmix/eda/basic.py
import json
import pandas as pd

from .utils import to_json, ColumnMixin


class BasicInfo(ColumnMixin):
    """
    Computes and summarizes basic information about a pandas DataFrame.

    Attributes:
        df (pd.DataFrame): The DataFrame to analyze.
        result (dict or None): Cached result of the last computation.

    Methods:
        compute() -> dict:
            Computes and returns basic statistics, data types, missing values, and summary statistics.
        to_json() -> str:
            Returns the computed information as a JSON string.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize BasicInfo with a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to analyze.
        """
        self.df = df
        self.result = None

    def compute(self) -> dict:
        """
        Compute basic information about the DataFrame.

        Returns:
            dict: A dictionary containing:
                - num_rows (int): Number of rows.
                - num_columns (int): Number of columns.
                - column_names (list): List of column names.
                - data_types (dict): Data types of columns.
                - missing_values (dict): Count of missing values per column.
                - summary_stats (dict): Descriptive statistics for numeric columns.
        """
        shape = self.df.shape
        columns = self._get_columns()
        dtypes = self.df.dtypes.apply(lambda x: str(x)).to_dict()
        missing = self.df.isnull().sum().to_dict()
        summary = self.df.describe().to_dict()

        self.result = {
            "num_rows": shape[0],
            "num_columns": shape[1],
            "column_names": columns,
            "data_types": dtypes,
            "missing_values": missing,
            "summary_stats": summary
        }
        return self.result

    def to_json(self) -> str:
        """
        Get the computed basic information as a JSON string.

        Returns:
            str: JSON-formatted string of the computed information.
        """
        if self.result is None:
            self.compute()
        return to_json(self.result)
