# src/owlmix/eda/charts/lag.py
import os
import matplotlib.pyplot as plt
import pandas as pd
from typing import TypedDict, NotRequired, Unpack
 
 
class LagCorrelationChartArgs(TypedDict):
    output_dir: str
    column: str
    lag: NotRequired[int]


class LagCorrelationChart:
    def __init__(self, df: pd.DataFrame, **kwargs: Unpack[LagCorrelationChartArgs]):
        self.df = df
        self.output_dir = kwargs.get("output_dir")
        self.column = kwargs.get("column")
        self.lag = kwargs.get("lag", 1)

        os.makedirs(self.output_dir, exist_ok=True)
 
    def generate(self) -> str:
        """
        Generates lag correlation plot for numeric columns.
        Returns saved file path.
        """
        series = self.df[self.column]
        lagged = series.shift(self.lag)
        df_lag = pd.DataFrame({
            "x": series,
            "y": lagged
        }).dropna()

        if df_lag.empty:
            raise ValueError("No data left after applying lag")

        plt.figure(figsize=(6, 6))
        plt.scatter(df_lag["x"], df_lag["y"], alpha=0.6)
 
        plt.xlabel(f"{self.column}")
        plt.ylabel(f"{self.column} (lag={self.lag})")
        plt.title("Lag Correlation")
 
        file_path = os.path.join(self.output_dir, f"lag_correlation_lag{self.lag}.png")
        plt.savefig(file_path)
        plt.close()
 
        return file_path
 
        numeric_df = self.df.select_dtypes(include="number")
 
        plt.figure(figsize=(8, 6))
 
        for col in numeric_df.columns:
            plt.scatter(
                numeric_df[col][:-self.lag],
                numeric_df[col].shift(self.lag).dropna(),
                label=col,
                alpha=0.6
            )
 
        plt.title(f"Lag Correlation (lag={self.lag})")
        plt.xlabel("Original")
        plt.ylabel("Lagged")
        plt.legend()
 
        file_path = os.path.join(self.output_dir, f"lag_correlation_lag{self.lag}.png")
        plt.savefig(file_path)
        plt.close()
 
        return file_path
