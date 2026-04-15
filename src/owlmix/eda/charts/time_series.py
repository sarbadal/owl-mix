# src/owlmix/eda/charts/timeseries.py
 
import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose


class TimeSeriesChart:
    def __init__(self, df, output_dir, columns=None, target=None, date_column=None, period=None, model="additive"):
        self.df = df
        self.output_dir = output_dir
        self.columns = columns
        self.target = target
        self.date_column = date_column
        self.period = period
        self.model = model

    def _validate(self):
        if self.date_column is None:
            raise ValueError("date_column must be provided for time series chart")

        if self.target is None:
            raise ValueError("target (value column) must be provided")

        if self.date_column not in self.df.columns:
            raise KeyError(f"date_column '{self.date_column}' not found")

        if self.target not in self.df.columns:
            raise KeyError(f"target column '{self.target}' not found")

    def _prepare_series(self):
        self._validate()

        df = self.df.copy()

        # Convert to datetime
        df[self.date_column] = pd.to_datetime(df[self.date_column], errors="coerce")

        # Drop invalid dates
        df = df.dropna(subset=[self.date_column])

        # Sort
        df = df.sort_values(self.date_column)

        # Set index
        df.set_index(self.date_column, inplace=True)

        # Extract numeric target
        series = pd.to_numeric(df[self.target], errors="coerce")

        # Drop NaNs
        series = series.dropna()

        if len(series) < 10:
            raise ValueError("Not enough data points")

        return series

    def _infer_period(self):
        """Infers seasonality period from date column."""
    
        if self.date_column is None:
            raise ValueError("date_column must be provided")
    
        # Step 1: prepare date column
        df = self.df.copy()
        df[self.date_column] = pd.to_datetime(df[self.date_column], errors="coerce")
    
        if df[self.date_column].isna().all():
            raise ValueError("date_column could not be converted to datetime")
    
        # Step 2: sort + set index
        df = df.sort_values(self.date_column)
        df = df.set_index(self.date_column)
    
        # Step 3: infer frequency from index
        freq = pd.infer_freq(df.index)
    
        if freq is None:
            return 12  # fallback
    
        freq = freq.lower()
    
        # Step 4: map to period
        if "d" in freq:
            return 7
        if "w" in freq:
            return 52
        if "m" in freq:
            return 12
        if "q" in freq:
            return 4
        if "h" in freq:
            return 24
        return 12  # safe fallback

    def _decompose(self, series):
        if self.period is None:
            self.period = self._infer_period()

        if len(series) < self.period * 2:
            raise ValueError(
                f"Need at least {self.period * 2} data points"
            )

        return seasonal_decompose(series, model=self.model, period=self.period)

    def _plot(self, result, file_path):
        fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

        axes[0].plot(result.observed)
        axes[0].set_title("Observed")

        axes[1].plot(result.trend)
        axes[1].set_title("Trend")

        axes[2].plot(result.seasonal)
        axes[2].set_title("Seasonality")

        axes[3].plot(result.resid)
        axes[3].set_title("Residual")

        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()
 
    def generate(self):
        try:
            series = self._prepare_series()
            result = self._decompose(series)

            file_path = os.path.join(
                self.output_dir,
                f"time_series_{self.target}.png"
            )

            self._plot(result, file_path)

            return file_path

        except Exception as e:
            print({
                "type": "time_series",
                "target": self.target,
                "error": str(e),
                "status": "failed"
            })
            raise 
