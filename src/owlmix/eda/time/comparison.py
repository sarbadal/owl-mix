# src/owlmix/eda/time/comparison.py
import pandas as pd
from typing import Callable

from owlmix.eda.utils import ColumnMixin, SerializableMixin

class TimeColumnRenamer:
    def rename_date_column(self, new_name: str = "date"):
        self.df = self.df.rename(columns={self.date_column: new_name})
        self.date_column = new_name


class TimeComparisonReport(ColumnMixin, SerializableMixin, TimeColumnRenamer):
    def __init__(self, df: pd.DataFrame, date_column: str, value_columns: list[str] = None, comparison_type: str = "yoy", agg_func: str = "sum", precision: int = 2):
        self.df = df.copy()
        self.date_column = date_column
        self.value_columns = self._get_columns(value_columns)
        self.comparison_type = comparison_type.lower()
        self.agg_func = agg_func
        self.precision = precision

        self.rename_date_column(new_name="date")
        self._validate()
        self._prepare()

    def _validate(self):
        if self.comparison_type not in ["yoy", "mom", "wow"]:
            raise ValueError(f"{self.comparison_type} not supported. Valid options are 'yoy' and 'mom' and 'wow'.")

    def _prepare(self):
        self.df[self.date_column] = pd.to_datetime(self.df[self.date_column])

        if self.comparison_type == "yoy":
            self.freq = "YE"

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

    def generate(self):
        self._aggregate()
        self._add_period_keys()
        self._compute_pct_change()

        return self._to_serializable(dt_format="%Y")


class TimeAggregatorReport(ColumnMixin, SerializableMixin, TimeColumnRenamer):
    def __init__(self, df, date_column: str, value_columns: list[str]=None, freq: str="YE", agg_func: str | Callable="sum", precision: int = 2):
        self.df = df.copy()
        self.date_column = date_column
        self.value_columns = self._get_columns(value_columns)
        self.freq = freq
        self.agg_func = agg_func
        self.precision = precision

        
        self.rename_date_column(new_name="date")
        self._validate()
        self._prepare()

    def _validate(self):
        valid_freq = {"D", "W", "ME", "Q", "YE"}

        if self.freq not in valid_freq:
            raise ValueError(f"freq must be one of {valid_freq}")

    def _prepare(self):
        self.df[self.date_column] = pd.to_datetime(self.df[self.date_column])

    def aggregate(self):
        df = self.df.set_index(self.date_column)

        self.df = (
            df[self.value_columns]
            .resample(self.freq)
            .agg(self.agg_func)
            .reset_index()
        )

        return self._to_serializable(dt_format="%Y-%m")
