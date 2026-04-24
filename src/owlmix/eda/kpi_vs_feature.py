# owlmix/eda/kpi_vs_feature.py
import pandas as pd

from .utils import ColumnMixin


class DualAxisLineChartDataGenerator(ColumnMixin):
    def __init__(self, df: pd.DataFrame, date_column: str, target_column: str, period: str = "monthly", columns: list[str] = None, agg_func: str = "sum"):
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
        self.period = period
        # self.date_format = date_format if date_format else "%Y-%m-%d"
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

    def _prepare_grouped_df(self):
        df = self.df.copy()

        # Step 1: Create formatted date column and sort date
        period_dates, formatted_dates = self._get_period_date_and_format(df[self.date_column])
        df["_formatted_date"] = formatted_dates
        df["_sort_date"] = period_dates

        # Step 2: Group by formatted date
        agg_columns = [self.target_column] + self.columns

        grouped = (
            df.groupby("_formatted_date")[agg_columns]
            .agg(self.agg_func)
            .reset_index()
        )

        # Step 3: Add sort date for proper sorting
        # Re-create sort dates for grouped data
        sort_dates = []
        for formatted in grouped["_formatted_date"]:
            if self.period == "weekly":
                sort_dates.append(pd.to_datetime(formatted + "-1", format="%G-W%V-%w"))
            elif self.period == "monthly":
                sort_dates.append(pd.to_datetime(formatted, format="%Y-%m"))
            elif self.period == "yearly":
                sort_dates.append(pd.to_datetime(formatted, format="%Y"))
            else:  # daily
                sort_dates.append(pd.to_datetime(formatted, format="%Y-%m-%d"))

        grouped["_sort_date"] = sort_dates
        grouped.sort_values("_sort_date", inplace=True)
        grouped.drop("_sort_date", axis=1, inplace=True)

        return grouped

    def generate(self):
        """Returns structured JSON for multiple dual-axis charts."""
        grouped = self._prepare_grouped_df()

        x_values = grouped["_formatted_date"].tolist()
        target_values = grouped[self.target_column].tolist()

        output = []

        for col in self.columns:
            if col not in grouped.columns:
                continue

            feature_values = grouped[col].tolist()

            output.append({
                "kpi": self.target_column,
                "column": col,
                "x": x_values,
                "target": target_values,
                "feature": feature_values
            })

        return {"data": output}