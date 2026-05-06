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

        def week_start(r): return r.start_time

        mapping = {
            "yoy":         (lambda dt: dt.dt.year, lambda dt: None),
            "mom":         (lambda dt: dt.dt.to_period("M").astype(str), lambda dt: None),
            "wow":         (lambda dt: dt.dt.to_period("W").apply(week_start), lambda dt: None),
            "qoq":         (lambda dt: dt.dt.to_period("Q").astype(str), lambda dt: None),
            "yoy_month":   (lambda dt: dt.dt.to_period("M").astype(str), lambda dt: dt.dt.month),
            "yoy_quarter": (lambda dt: dt.dt.to_period("Q").astype(str), lambda dt: dt.dt.quarter),
            "yoy_week":    (lambda dt: dt.dt.to_period("W").apply(week_start), lambda dt: dt.dt.isocalendar().week),
        }

        if self.comparison_type not in mapping:
            raise ValueError(f"Unsupported comparison_type: {self.comparison_type}")

        year_func, period_func = mapping[self.comparison_type]
        self.df["year"] = year_func(dt)
        self.df["period"] = period_func(dt) if period_func(dt) is not None else None

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
