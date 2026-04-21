# owlmix/eda/kpi_vs_feature.py
import pandas as pd

from .utils import ColumnMixin


class DualAxisLineChartDataGenerator(ColumnMixin):
    def __init__(self, df: pd.DataFrame, date_column: str, target_column: str, date_format: str = None, columns: list[str] = None, agg_func: str = "sum"):
        self.df = df.copy()
        self.date_column = date_column
        self.date_format = date_format if date_format else "%Y-%m-%d"
        self.target_column = target_column
        self.columns = [col for col in self._get_columns(columns) if col != self.target_column]
        self.agg_func = agg_func

        # Ensure datetime
        self.df[self.date_column] = pd.to_datetime(self.df[self.date_column])

    def _prepare_grouped_df(self):
        df = self.df.copy()

        # Step 1: Create formatted date column
        df["_formatted_date"] = df[self.date_column].dt.strftime(self.date_format)

        # Step 2: Group by formatted date
        agg_columns = [self.target_column] + self.columns

        grouped = (
            df.groupby("_formatted_date")[agg_columns]
            .agg(self.agg_func)
            .reset_index()
        )

        # Step 3: Sort properly (important!)
        grouped["_sort_date"] = pd.to_datetime(grouped["_formatted_date"])
        grouped.sort_values("_sort_date", inplace=True)

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
                "column": col,
                "x": x_values,
                "target": target_values,
                "feature": feature_values
            })

        return {"data": output}
