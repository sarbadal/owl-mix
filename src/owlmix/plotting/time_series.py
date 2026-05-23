import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from statsmodels.tsa.seasonal import seasonal_decompose, DecomposeResult

@dataclass
class TimeSeriesPlotParams:
    date_column: str
    target_column: str
    period: int = 12
    model: str = "additive"  # "additive" or "multiplicative"
    dpi: int = 150
    figsize: tuple[float, float] = (24.0, 4.0)
    filename_prefix: str = "time_series_decomposition"


class TimeSeriesPlotter:
    FREQ_MAP = {
        "d": 7,
        "w": 52,
        "m": 12,
        "q": 4,
        "h": 24
    }
    def __init__(self, df: pd.DataFrame, params: TimeSeriesPlotParams):
        self.df = df.copy()
        self.params = params

    def plot(self, output_dir: str = "outputs/charts") -> str:
        series = self._prepare_series()
        decomposition = self._decompose(series)
        observed_path = self._plot_observed(decomposition.observed, output_dir)
        trend_path = self._plot_trend(decomposition.trend, output_dir)
        seasonal_path = self._plot_seasonal(decomposition.seasonal, output_dir)
        resid_path = self._plot_residual(decomposition.resid, output_dir)
        return {
            "observed": observed_path,
            "trend": trend_path,
            "seasonal": seasonal_path,
            "residuals": resid_path
        }

    def _validate(self) -> None:
        if not self.params.date_column:
            raise ValueError("date_column must be provided for time series chart")
        if not self.params.target_column:
            raise ValueError("target (value column) must be provided")
        if self.params.date_column not in self.df.columns:
            raise KeyError(f"date_column '{self.params.date_column}' not found")
        if self.params.target_column not in self.df.columns:
            raise KeyError(f"target column '{self.params.target_column}' not found")

    def _prepare_series(self) -> pd.Series:
        """Prepare and clean the time series data."""
        self._validate()
        df = self.df.copy()
        df[self.params.date_column] = pd.to_datetime(df[self.params.date_column], errors="coerce")
        df = df.dropna(subset=[self.params.date_column])
        df = df.sort_values(self.params.date_column)
        df.set_index(self.params.date_column, inplace=True)
        series = pd.to_numeric(df[self.params.target_column], errors="coerce").dropna()
        if len(series) < 10:
            raise ValueError("Not enough data points")
        return series

    def _infer_period(self) -> int:
        """Dynamically infers seasonality period from date column."""
        df = self.df.copy()
        df[self.params.date_column] = pd.to_datetime(df[self.params.date_column], errors="coerce")
        df = df.dropna(subset=[self.params.date_column])
        df = df.sort_values(self.params.date_column)
        df.set_index(self.params.date_column, inplace=True)
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
        if self.params.period is None:
            self.params.period = self._infer_period()
        if len(series) < self.params.period * 2:
            raise ValueError(f"Need at least {self.params.period * 2} data points")
        decomposed = seasonal_decompose(series, model=self.params.model, period=self.params.period)
        return decomposed

    def _plot_observed(self, observed: pd.Series, output_dir: str) -> str:
        fig, ax = plt.subplots(figsize=self.params.figsize)
        self._apply_theme(fig, ax)
        observed.plot(ax=ax)
        ax.set_title("Observed")
        ax.set_xlabel("Date")
        ax.set_ylabel(self.params.target_column)
        file_path = os.path.join(output_dir, f"{self.params.filename_prefix}_observed.png")
        self._save_figure(fig, file_path, "observed")
        return file_path

    def _plot_trend(self, trend: pd.Series, output_dir: str) -> str:
        fig, ax = plt.subplots(figsize=self.params.figsize)
        self._apply_theme(fig, ax)
        trend.plot(ax=ax)
        ax.set_title("Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Trend")
        file_path = os.path.join(output_dir, f"{self.params.filename_prefix}_trend.png")
        self._save_figure(fig, file_path, "trend")
        return file_path

    def _plot_seasonal(self, seasonal: pd.Series, output_dir: str) -> str:
        fig, ax = plt.subplots(figsize=self.params.figsize)
        self._apply_theme(fig, ax)
        seasonal.plot(ax=ax)
        ax.set_title("Seasonality")
        ax.set_xlabel("Date")
        ax.set_ylabel("Seasonality")
        file_path = os.path.join(output_dir, f"{self.params.filename_prefix}_seasonal.png")
        self._save_figure(fig, file_path, "seasonal")
        return file_path

    def _plot_residual(self, resid: pd.Series, output_dir: str) -> str:
        fig, ax = plt.subplots(figsize=self.params.figsize)
        self._apply_theme(fig, ax)
        resid.plot(ax=ax)
        ax.set_title("Residuals")
        ax.set_xlabel("Date")
        ax.set_ylabel("Residuals")
        file_path = os.path.join(output_dir, f"{self.params.filename_prefix}_residuals.png")
        self._save_figure(fig, file_path, "residuals")
        return file_path

    def _apply_theme(self, fig: plt.Figure, ax: plt.Axes) -> None:
        def _resolve_color(value, fallback):
            if value is None:
                return fallback
            if isinstance(value, str) and value.lower() in {"auto", "inherit", "none"}:
                return fallback
            return value

        text_color = plt.rcParams.get("text.color", "black")
        fig_color = _resolve_color(plt.rcParams.get("figure.facecolor", "white"), "white")
        axes_color = _resolve_color(plt.rcParams.get("axes.facecolor", "white"), "white")
        title_color = _resolve_color(plt.rcParams.get("axes.titlecolor"), text_color)
        label_color = _resolve_color(plt.rcParams.get("axes.labelcolor"), text_color)
        tick_color = _resolve_color(plt.rcParams.get("xtick.color"), text_color)
        spine_color = _resolve_color(plt.rcParams.get("axes.edgecolor"), tick_color)

        fig.patch.set_facecolor(fig_color)
        ax.set_facecolor(axes_color)
        ax.title.set_color(title_color)
        ax.xaxis.label.set_color(label_color)
        ax.yaxis.label.set_color(label_color)
        ax.tick_params(axis="x", colors=tick_color)
        ax.tick_params(axis="y", colors=tick_color)

        for spine in ax.spines.values():
            spine.set_color(spine_color)

    def _save_figure(self, fig: plt.Figure, output_path: str, component: str) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fig.savefig(
            output_path, 
            dpi=self.params.dpi,
            bbox_inches="tight",
            transparent=True,
            facecolor=fig.get_facecolor()
        )
        plt.close(fig)
        return output_path