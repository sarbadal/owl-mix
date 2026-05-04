# src/owlmix/eda/charts/timeseries.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose, DecomposeResult
from typing import TypedDict, NotRequired, Unpack


class TimeSeriesChartArgs(TypedDict):
    output_dir: str
    columns: NotRequired[list[str]]
    target: NotRequired[str]
    date_column: NotRequired[str]
    period: NotRequired[int]
    model: NotRequired[str]


class TimeSeriesChart:
    FREQ_MAP = {
        "d": 7,
        "w": 52,
        "m": 12,
        "q": 4,
        "h": 24
    }

    def __init__(self, df: pd.DataFrame, **kwargs: Unpack[TimeSeriesChartArgs]):
        """Initializes the TimeSeriesChart with the given DataFrame and configuration."""
        self.df = df
        self.output_dir = kwargs.get("output_dir")
        self.columns = kwargs.get("columns")
        self.target = kwargs.get("target")
        self.date_column = kwargs.get("date_column")
        self.period = kwargs.get("period")
        self.model = kwargs.get("model", "additive")

    def _validate(self) -> None:
        if not self.date_column:
            raise ValueError("date_column must be provided for time series chart")
        if not self.target:
            raise ValueError("target (value column) must be provided")
        if self.date_column not in self.df.columns:
            raise KeyError(f"date_column '{self.date_column}' not found")
        if self.target not in self.df.columns:
            raise KeyError(f"target column '{self.target}' not found")

    def _prepare_series(self) -> pd.Series:
        """Prepare and clean the time series data."""
        self._validate()
        df = self.df.copy()
        df[self.date_column] = pd.to_datetime(df[self.date_column], errors="coerce")
        df = df.dropna(subset=[self.date_column])
        df = df.sort_values(self.date_column)
        df.set_index(self.date_column, inplace=True)
        series = pd.to_numeric(df[self.target], errors="coerce").dropna()
        if len(series) < 10:
            raise ValueError("Not enough data points")
        return series

    def _infer_period(self) -> int:
        """Dynamically infers seasonality period from date column."""
        df = self.df.copy()
        df[self.date_column] = pd.to_datetime(df[self.date_column], errors="coerce")
        df = df.dropna(subset=[self.date_column])
        df = df.sort_values(self.date_column)
        df.set_index(self.date_column, inplace=True)
        freq = pd.infer_freq(df.index)

        if freq:
            freq = freq.lower()
            for key, period in self.FREQ_MAP.items():
                if key in freq:
                    return period

        diffs = df.index.to_series().diff().dropna()
        if not diffs.empty:
            most_common = diffs.mode()[0]
            if pd.Timedelta(days=1) <= most_common < pd.Timedelta(days=8):
                return 7
            if pd.Timedelta(weeks=1) <= most_common < pd.Timedelta(days=32):
                return 12
            if pd.Timedelta(days=28) <= most_common < pd.Timedelta(days=92):
                return 4
            if pd.Timedelta(days=355) < most_common < pd.Timedelta(days=375):
                return 1
        return 12

    def _decompose(self, series: pd.Series) -> DecomposeResult:
        """Decompose the time series into trend, seasonal, and residuals."""
        if self.period is None:
            self.period = self._infer_period()
        if len(series) < self.period * 2:
            raise ValueError(f"Need at least {self.period * 2} data points")
        return seasonal_decompose(series, model=self.model, period=self.period)

    def _plot(self, result: DecomposeResult, file_path: str) -> None:
        """Plot the decomposition results and save to file."""
        fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
        titles = ["Observed", "Trend", "Seasonality", "Residual"]
        data = [result.observed, result.trend, result.seasonal, result.resid]
        for ax, title, series in zip(axes, titles, data):
            ax.plot(series)
            ax.set_title(f"{title} (model={self.model}, period={self.period})" if title != "Observed" else title)
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()
 
    def generate(self) -> str:
        """Generate and save the time series decomposition chart."""
        try:
            series = self._prepare_series()
            result = self._decompose(series)
            file_path = os.path.join(self.output_dir, f"time_series_{self.target}.png")
            self._plot(result, file_path)
            return file_path
        except Exception as e:
            logger.error({
                "type": "time_series",
                "target": self.target,
                "error": str(e),
                "status": "failed"
            })
            raise