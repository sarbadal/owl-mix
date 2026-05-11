import json
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Any, List, Optional, Dict
from pandas.core.dtypes.base import ExtensionDtype


class ColumnMixin:
    """
    Mixin to extract numeric and categorical columns from a pandas DataFrame.

    Assumes the inheriting class has a `self.df` attribute of type `pd.DataFrame`.
    """

    def _get_numeric_columns(self, value_columns: Optional[List[str]] = None) -> List[str]:
        """
        Returns a list of numeric column names from the DataFrame.
        If `value_columns` is provided, only those columns are considered.

        Args:
            value_columns (Optional[List[str]]): List of column names to filter.

        Returns:
            List[str]: List of numeric column names.

        Raises:
            AttributeError: If self.df is not set or not a DataFrame.
            ValueError: If no valid or numeric columns are found.
        """
        if not hasattr(self, "df") or not isinstance(self.df, pd.DataFrame):
            raise AttributeError("The object must have a 'df' attribute of type pandas.DataFrame.")

        if value_columns:
            valid_columns = [col for col in self.df.columns if col in value_columns]
            if not valid_columns:
                raise ValueError(
                    f"None of the specified columns {value_columns} are present in the DataFrame."
                )
            numeric_cols = self.df[valid_columns].select_dtypes(include=["number"]).columns.tolist()
            if not numeric_cols:
                raise ValueError(
                    f"None of the provided columns {valid_columns} are numeric."
                )
            return numeric_cols

        return self.df.select_dtypes(include=["number"]).columns.tolist()

    def _get_categorical_columns(self, value_columns: Optional[List[str]] = None) -> List[str]:
        """
        Returns a list of categorical column names from the DataFrame.
        If `value_columns` is provided, only those columns are considered.

        Args:
            value_columns (Optional[List[str]]): List of column names to filter.

        Returns:
            List[str]: List of categorical column names.

        Raises:
            AttributeError: If self.df is not set or not a DataFrame.
            ValueError: If no valid or categorical columns are found.
        """
        if not hasattr(self, "df") or not isinstance(self.df, pd.DataFrame):
            raise AttributeError("The object must have a 'df' attribute of type pandas.DataFrame.")

        if value_columns:
            valid_columns = [col for col in self.df.columns if col in value_columns]
            if not valid_columns:
                raise ValueError(
                    f"None of the specified columns {value_columns} are present in the DataFrame."
                )
            categorical_cols = self.df[valid_columns].select_dtypes(exclude=["number"]).columns.tolist()
            if not categorical_cols:
                raise ValueError(
                    f"None of the provided columns {valid_columns} are categorical."
                )
            return categorical_cols

        return self.df.select_dtypes(exclude=["number"]).columns.tolist()
