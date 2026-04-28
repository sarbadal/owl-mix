# owlmix/eda/categorical_distribution_generator.py
import pandas as pd
import numpy as np

from .utils import CategoricalColumnMixin


class CategoricalDistributionGenerator(CategoricalColumnMixin):
    """
    Generates bell-shaped categorical distributions for specified columns in a DataFrame.

    This class arranges the categories of each column such that the most frequent category
    is centered, and the remaining categories alternate to the left and right, creating a
    bell-shaped distribution for visualization purposes.

    Attributes:
        df (pd.DataFrame): The input DataFrame.
        columns (list[str]): List of columns to generate distributions for.
    """

    def __init__(self, df: pd.DataFrame, columns: list[str] = None):
        """
        Initialize the generator with a DataFrame and optional list of columns.

        Args:
            df (pd.DataFrame): The input DataFrame.
            columns (list[str], optional): Columns to generate distributions for.
                If None, uses all categorical columns.
        """
        self.df = df.copy()
        self.columns = self._get_columns(columns)

    def _arrange_bell_shape(self, categories: list[str], counts: list[int]) -> tuple[list[str], list[int]]:
        """
        Arrange categories and counts in a bell shape: highest frequency in the center,
        others alternate left and right.

        Args:
            categories (list[str]): List of category names, sorted by frequency descending.
            counts (list[int]): Corresponding counts for each category.

        Returns:
            tuple[list[str], list[int]]: Categories and counts arranged in bell shape.
        """
        n = len(categories)
        arranged = [None] * n
        center = n // 2
        left = center - 1
        right = center + 1

        arranged[center] = (categories[0], counts[0])
        place_right = True

        for i in range(1, n):
            if place_right and right < n:
                arranged[right] = (categories[i], counts[i])
                right += 1
            elif left >= 0:
                arranged[left] = (categories[i], counts[i])
                left -= 1
            place_right = not place_right

        cats, vals = zip(*arranged)
        return list(cats), list(vals)

    def generate(self) -> dict:
        """
        Generate bell-shaped categorical distributions for all specified columns.

        Returns:
            dict: A dictionary with a "data" key containing a list of distributions,
                  each as returned by generate_for_column.
        """
        result = [self.generate_for_column(column) for column in self.columns]
        return {"data": result}

    def generate_for_column(self, column: str) -> dict:
        """
        Generate a bell-shaped categorical distribution for a single column.

        Args:
            column (str): The column name.

        Returns:
            dict: {
                "column": column_name,
                "x": [categories in bell shape order],
                "y": [counts in bell shape order]
            }
        """
        value_counts = self.df[column].value_counts()
        categories = value_counts.index.tolist()
        counts = value_counts.values.tolist()

        cats_arr, counts_arr = self._arrange_bell_shape(categories, counts)

        return {
            "column": column,
            "x": cats_arr,
            "y": counts_arr
        }
 