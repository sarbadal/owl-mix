# src/owlmix/eda/categorical_distribution_generator.py
import pandas as pd
import numpy as np

from owlmix.eda.utils import CategoricalColumnMixin

 
class CategoricalDistributionGenerator(CategoricalColumnMixin):
    def __init__(self, df: pd.DataFrame, columns: list[str] = None):
        self.df = df.copy()
        self.columns = self._get_columns(columns)
 
    def _arrange_bell_shape(self, categories: list[str], counts: list[int]) -> tuple[list[str], list[int]]:
        """Arrange categories so that highest freq is center, others alternate left-right."""
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
 
        # unzip
        cats, vals = zip(*arranged)
        return list(cats), list(vals)

    def generate(self) -> dict:
        result = []
        for column in self.columns:
            result.append(self.generate_for_column(column))
        return {"data": result}
 
    def generate_for_column(self, column: str) -> dict:
        """
        Returns:
            {
                "column": column_name,
                "x": [...categories...],
                "y": [...counts...]
            }
        """
 
        # Count frequencies
        value_counts = self.df[column].value_counts()
 
        categories = value_counts.index.tolist()
        counts = value_counts.values.tolist()
 
        # Arrange into bell shape
        cats_arr, counts_arr = self._arrange_bell_shape(
            categories=categories, 
            counts=counts
        )
 
        return {
            "column": column,
            "x": cats_arr,
            "y": counts_arr
        }
 