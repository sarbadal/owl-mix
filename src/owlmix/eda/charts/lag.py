# src/owlmix/eda/charts/lag.py
 
import os
import matplotlib.pyplot as plt
import pandas as pd
 
 
class LagCorrelationChart:
    def __init__(self, df: pd.DataFrame, column: str, output_dir: str = "charts", lag: int = 1):
        self.df = df
        self.output_dir = output_dir
        self.column = column
        self.lag = lag

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
