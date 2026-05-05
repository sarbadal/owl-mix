# owlmix/eda/kpi_vs_feature.py
import pandas as pd
from typing import Dict, Any

from .utils import ColumnMixin
from ..typing.types import PeriodType
from ..typing.normalize import normalize_period


class DualAxisLineChartDataGenerator(ColumnMixin):
    """Generates data for dual-axis line charts comparing a KPI to multiple features over time."""
    def __init__(self, df: pd.DataFrame, date_column: str, target_column: str, period: PeriodType = "monthly", columns: list[str] = None, agg_func: str = "sum"):
        """
        Args:
            df: DataFrame
            date_column: Name of date column
            target_column: KPI column to plot
            period: Grouping period - "daily", "weekly", "monthly", "yearly"
            columns: Feature columns to compare
            agg_func: Aggregation function ("sum", "mean", "max", etc.)
        """
        self.df = df.copy()
        self.date_column = date_column
        self.period = normalize_period(period)
        self.target_column = target_column
        self.columns = [col for col in self._get_columns(columns) if col != self.target_column]
        self.agg_func = agg_func

        # Ensure datetime
        self.df[self.date_column] = pd.to_datetime(self.df[self.date_column])

    def _get_period_date_and_format(self, series):
        """Generate period date and formatted string based on period type."""
        if self.period == "weekly":
            # Get Monday of each week (start of week)
            period_dates = series.dt.to_period('W').dt.start_time
            formatted = period_dates.dt.strftime("%Y-W%V")  # e.g., "2024-W10"
            return period_dates, formatted

        if self.period == "monthly":
            # Get first day of each month
            period_dates = series.dt.to_period('M').dt.start_time
            formatted = period_dates.dt.strftime("%Y-%m")  # e.g., "2024-01"
            return period_dates, formatted

        if self.period == "yearly":
            # Get first day of each year
            period_dates = series.dt.to_period('Y').dt.start_time
            formatted = period_dates.dt.strftime("%Y")  # e.g., "2024"
            return period_dates, formatted

        period_dates = series
        formatted = period_dates.dt.strftime("%Y-%m-%d")
        return period_dates, formatted

    def _prepare_grouped_df(self) -> pd.DataFrame:
        """Prepare and group the DataFrame by the specified period."""
        df = self.df.copy()
        period_dates, formatted_dates = self._get_period_date_and_format(df[self.date_column])
        df["_formatted_date"] = formatted_dates
        df["_sort_date"] = period_dates

        agg_columns = [self.target_column] + self.columns
        grouped = (
            df.groupby("_formatted_date")[agg_columns]
            .agg(self.agg_func)
            .reset_index()
        )

        # Add sort date for proper sorting
        def parse_sort_date(formatted: str) -> pd.Timestamp:
            if self.period == "weekly":
                return pd.to_datetime(formatted + "-1", format="%G-W%V-%w")
            elif self.period == "monthly":
                return pd.to_datetime(formatted, format="%Y-%m")
            elif self.period == "yearly":
                return pd.to_datetime(formatted, format="%Y")
            else:
                return pd.to_datetime(formatted, format="%Y-%m-%d")

        grouped["_sort_date"] = grouped["_formatted_date"].apply(parse_sort_date)
        grouped = grouped.sort_values("_sort_date").drop("_sort_date", axis=1)
        return grouped

    def generate(self) -> Dict[str, Any]:
        """
        Returns:
            Structured JSON for multiple dual-axis charts.
        """
        grouped = self._prepare_grouped_df()
        x_values = grouped["_formatted_date"].tolist()
        target_values = grouped[self.target_column].tolist()

        output = []
        for col in self.columns:
            if col in grouped.columns:
                feature_values = grouped[col].tolist()
                output.append({
                    "kpi": self.target_column,
                    "column": col,
                    "x": x_values,
                    "target": target_values,
                    "feature": feature_values
                })

        return {"data": output}