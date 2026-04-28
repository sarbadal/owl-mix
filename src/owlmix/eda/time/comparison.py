# src/owlmix/eda/time/comparison.py
import pandas as pd
from typing import Self, TypedDict, Unpack, NotRequired, Callable

from owlmix.typing.types import ComparisonType
from owlmix.typing.normalize import normalize_comparison_type
from owlmix.eda.utils import ColumnMixin, SerializableMixin


class ComparisonSettings(TypedDict):
    comparison_type: NotRequired[ComparisonType]
    agg_func: NotRequired[str]
    precision: NotRequired[int]


class TimeColumnRenamer:
    def rename_date_column(self, new_name: str = "date"):
        self.df = self.df.rename(columns={self.date_column: new_name})
        self.date_column = new_name


class TimeComparisonReport(ColumnMixin, SerializableMixin, TimeColumnRenamer):
    def __init__(self, df: pd.DataFrame, date_column: str, value_columns: list[str] = None, **other_settings: Unpack[ComparisonSettings]):
        self.df = df.copy()
        self.date_column = date_column
        self.value_columns = self._get_columns(value_columns)

        # Get settings from the **other_settings
        self.comparison_type = normalize_comparison_type(
            other_settings.get("comparison_type", "yoy")
        )
        self.agg_func = other_settings.get("agg_func", "sum")
        self.precision = other_settings.get("precision", 2)

        self.rename_date_column(new_name="date")
        self._validate()

    def _validate(self):
        options = ["yoy", "qoq", "mom", "wow", "yoy_month", "yoy_quarter", "yoy_week"]
        if self.comparison_type not in options:
            raise ValueError(f"{self.comparison_type} not supported. Valid options are {options}")

    def _aggregate(self):
        group_cols = ["year"]
        if "period" in self.df.columns.tolist() and self.df["period"].notna().any():
            group_cols.append("period")

        self.df = (
            self.df
            .groupby(group_cols, as_index=False)[self.value_columns]
            .sum()  # or mean(), depending on your use case
        )

    def _add_period_keys(self):
        dt = pd.to_datetime(self.df[self.date_column], errors="coerce")

        # Aggregate at YEAR level
        if self.comparison_type == "yoy":
            self.df["year"] = dt.dt.year  # e.g., 2024
            self.df["period"] = None  # not needed for YoY
            return None

        # Aggregate at YEAR-MONTH level
        if self.comparison_type == "mom":
            self.df["year"] = dt.dt.to_period("M").astype(str)  # e.g., 2024-01
            self.df["period"] = None  # sequential comparison
            return None

        # Aggregate at WEEK level (use week start date)
        if self.comparison_type == "wow":
            week_period = dt.dt.to_period("W")
            self.df["year"] = week_period.apply(lambda r: r.start_time)  # clean x-axis
            self.df["period"] = None  # sequential comparison
            return None

        # Aggregate at Quarter level
        if self.comparison_type == "qoq":
            self.df["year"] = dt.dt.to_period("Q").astype(str)
            self.df["period"] = None
            return None

        # YOY (MONTH LEVEL) → Jan vs Jan last year
        if self.comparison_type == "yoy_month":
            self.df["year"] = dt.dt.year
            self.df["period"] = dt.dt.month
            return None

        # YOY (QUARTER LEVEL) → Q1 vs Q1 last year
        if self.comparison_type == "yoy_quarter":
            self.df["year"] = dt.dt.year
            self.df["period"] = dt.dt.quarter
            return None

        # YOY (WEEK LEVEL) → Week 32 vs Week 32 last year
        if self.comparison_type == "yoy_week":
            iso = dt.dt.isocalendar()
            self.df["year"] = iso.year
            self.df["period"] = iso.week.astype(int)
            return None

        raise ValueError(f"Unsupported comparison_type: {self.comparison_type}")

    def _compute_pct_change(self):
        self.df = self.df.sort_values(["year", "period"] if "period" in self.df else ["year"])

        for col in self.value_columns:
            if self.comparison_type in ["yoy_month", "yoy_quarter", "yoy_week"]:
                # Compare same period across years
                self.df[f"{col}_pct_change"] = self.df.groupby("period")[col].pct_change() * 100
            else:
                # Sequential comparison
                self.df[f"{col}_pct_change"] = self.df[col].pct_change() * 100

    def generate(self):
        self._add_period_keys()
        self._aggregate()
        self._compute_pct_change()

        return self._to_serializable()


# NOT IN USE
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

        return self._to_serializable()
