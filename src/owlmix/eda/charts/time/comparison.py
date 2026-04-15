import os
import pandas as pd
import matplotlib.pyplot as plt


class ComparisonChart:
    def __init__(self, df: pd.DataFrame, date_column: str, value_columns: list[str], freq: str = "ME", comparison: str = "mom", output_dir: str = "outputs"):
        self.df = df.copy()
        self.date_column = date_column
        self.value_columns = value_columns
        self.freq = freq
        self.comparison = comparison.lower()
        self.output_dir = output_dir


    def _prepare(self):
        self.df[self.date_column] = pd.to_datetime(self.df[self.date_column])
        self.df = self.df.set_index(self.date_column)

    def _aggregate(self):
        return (
            self.df[self.value_columns]
            .resample(self.freq)
            .sum()
            .sort_index()
        )

    def _compute_change(self, df):
        if self.comparison == "mom":
            return df.pct_change() * 100
        if self.comparison == "yoy":
            return df.pct_change(periods=12) * 100
        if self.comparison == "wow":
            return df.pct_change(periods=1) * 100

        raise ValueError("comparison must be one of ['mom', 'yoy', 'wow']")

    def generate(self):
        self._prepare()

        aggregated = self._aggregate()
        comparison_df = self._compute_change(aggregated)

        os.makedirs(self.output_dir, exist_ok=True)

        file_path = os.path.join(
            self.output_dir,
            f"{self.comparison}_comparison.png"
        )

        plt.figure(figsize=(12, 6))

        for col in comparison_df.columns:
            plt.plot(comparison_df.index, comparison_df[col], label=col)

        plt.title(f"{self.comparison.upper()} Comparison (%)")
        plt.xlabel("Date")
        plt.ylabel("Percentage Change")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()

        return file_path