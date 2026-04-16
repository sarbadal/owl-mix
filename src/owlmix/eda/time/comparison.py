# src/owlmix/eda/time/comparison.py
import pandas as pd

from owlmix.eda.utils import ColumnMixin


class TimeComparisonReport(ColumnMixin):
    def __init__(self, df: pd.DataFrame, date_column: str, value_columns: list[str] = None, comparison_type: str = "yoy", agg_func: str = "sum", precision: int = 2):
        self.df = df.copy()
        self.date_column = date_column
        self.value_columns = self._get_columns(value_columns)
        self.comparison_type = comparison_type.lower()
        self.agg_func = agg_func
        self.precision = precision

        self._validate()
        self._prepare()

    def _validate(self):
        if self.comparison_type not in ["yoy", "mom", "wow"]:
            raise ValueError(f"{self.comparison_type} not supported. Valid options are 'yoy' and 'mom' and 'wow'.")

    def _prepare(self):
        self.df[self.date_column] = pd.to_datetime(self.df[self.date_column])

        if self.comparison_type == "yoy":
            self.freq = "ME"

        if self.comparison_type == "mom":
            self.freq = "ME"

        if self.comparison_type == "wow":
            self.freq = "W"

    def _aggregate(self):
        df = self.df.set_index(self.date_column)

        self.df = (
            df[self.value_columns]
            .resample(self.freq)
            .agg(self.agg_func)
            .reset_index()
        )

    def _add_period_keys(self):
        if self.comparison_type in ["yoy", "mom"]:
            self.df["year"] = self.df[self.date_column].dt.year
            self.df["period"] = self.df[self.date_column].dt.month

        if self.comparison_type == "wow":
            self.df["year"] = self.df[self.date_column].dt.year
            self.df["period"] = (
                self.df[self.date_column]
                .dt.isocalendar()
                .week.astype(int)
            )

    def _compute_pct_change(self):
        self.df = self.df.sort_values(["period", "year"])

        for col in self.value_columns:
            self.df[f"{col}_pct_change"] = (
                self.df.groupby("period")[col]
                .pct_change()*100
            )

    def _to_serializable(self):
        return {
            "frequency": self.freq,
            "columns": self.value_columns,
            "data": [
                {
                    "date": str(idx),
                    **{k: self._safe(v) for k, v in row.items()}
                }
                for idx, row in self.df.iterrows()
            ]
        }

    def _safe(self, val):
        if pd.isna(val):
            if isinstance(val, (pd.Timestamp, pd.DatetimeIndex)):
                return "1970-01-01"
            return None

        if isinstance(val, (pd.Timestamp, pd.DatetimeIndex)):
            return val.strftime("%Y-%m-%d")

        if isinstance(val, (str, int, float)):
            rounded = round(float(val), self.precision)

            if rounded.is_integer():
                return int(rounded)

            return rounded

        return str(val)

    def generate(self):
        self._validate()
        self._prepare()
        self._aggregate()
        self._add_period_keys()
        self._compute_pct_change()

        return self._to_serializable()
