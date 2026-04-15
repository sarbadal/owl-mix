# src/owlmix/eda/time/comparison.py
import pandas as pd

from owlmix.eda.utils import ColumnMixin


class TimeComparisonReport(ColumnMixin):
    def __init__(self, df: pd.DataFrame, date_column: str, value_columns: list[str]=None, freq=None):
        self.df = df.copy()
        self.date_column = date_column
        self.value_columns = self._get_columns(value_columns)
        self.freq = freq

    def _validate(self):
        if self.date_column not in self.df.columns:
            raise ValueError(f"{self.date_column} not found in dataframe")

        missing_cols = [c for c in self.value_columns if c not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Columns not found: {missing_cols}")

    def _prepare_datetime(self):
        self.df[self.date_column] = pd.to_datetime(self.df[self.date_column])

    def _aggregate(self):
        df = self.df.set_index(self.date_column)

        grouped = (
            df[self.value_columns]
            .resample(self.freq)
            .sum()
            .sort_index()
        )

        return grouped

    def _compute_change(self, grouped):
        result = grouped.copy()

        for col in self.value_columns:
            result[f"{col}_pct_change"] = grouped[col].pct_change() * 100

        return result

    def generate(self):
        self._validate()
        self._prepare_datetime()

        inferred_freq = self._infer_freq() if self.freq is None else self.freq
        self.freq = inferred_freq or "ME"

        grouped = self._aggregate()
        result = self._compute_change(grouped)

        return self._to_serializable(result)

    def _to_serializable(self, df):
        return {
            "frequency": self.freq,
            "columns": self.value_columns,
            "data": [
                {
                    "date": str(idx),
                    **{k: self._safe(v) for k, v in row.items()}
                }
                for idx, row in df.iterrows()
            ]
        }

    def _safe(self, val):
        if pd.isna(val):
            return None
        return float(val)

    def _infer_freq(self) -> str:
        try:
            inferred_freq = pd.infer_freq(self.df[self.date_column])
            return inferred_freq
        except Exception as e:
            print(e)
            return None
