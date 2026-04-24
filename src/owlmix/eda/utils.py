# src/owlmix/eda/utils.py
import json
import os

import numpy as np
import pandas as pd
from datetime import datetime
from pandas.core.dtypes.base import ExtensionDtype


class CategoricalColumnMixin:
    def _get_columns(self, columns: list[str] = None):
        if columns:
            valid_columns = [col for col in self.df.columns if col in columns]

            if not valid_columns:
                raise ValueError("None of the columns available in the dataframe are valid.")

            return valid_columns

        return self.df.select_dtypes(include=["object", "category"]).columns.tolist()


class ColumnMixin:
    def _get_columns(self, value_columns: list[str] = None):
        if value_columns:
            valid_columns = [col for col in self.df.columns if col in value_columns]

            if not valid_columns:
                raise ValueError("None of the columns available in the dataframe are valid.")

            numeric_cols = self.df[valid_columns].select_dtypes(include=["number"]).columns.tolist()

            if not numeric_cols:
                raise ValueError("None of the provided columns are not numeric")

            return numeric_cols

        return self.df.select_dtypes(include=["number"]).columns.tolist()


class SerializableMixin:
    def _to_serializable(self, dt_format: str="%Y-%m-%d"):
        result = {
            "frequency": self.freq,
            "columns": self.value_columns,
            "data": [
                {
                    "date": str(idx),
                    **{k: self._safe(v, dt_format=dt_format) for k, v in row.items()}
                }
                for idx, row in self.df.iterrows()
            ]
        }

        return result

    def _safe(self, val, dt_format: str="%Y-%m-%d"):
        if pd.isna(val):
            if isinstance(val, (pd.Timestamp, pd.DatetimeIndex)):
                return "1970-01-01"
            return None

        if isinstance(val, (pd.Timestamp, pd.DatetimeIndex)):
            return val.strftime(dt_format)

        if isinstance(val, (str, int, float)):
            rounded = round(float(val), self.precision)

            if rounded.is_integer():
                return int(rounded)

            return rounded

        return str(val)
 
 
class NumpyPandasEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle numpy and pandas data types."""
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        if isinstance(obj, (pd.Timestamp, datetime)):
            return obj.isoformat()
        if isinstance(obj, (pd.Series,)):
            return obj.to_dict()
        if isinstance(obj, (pd.DataFrame,)):
            return obj.to_dict(orient="records")
        if isinstance(obj, (np.dtype, ExtensionDtype)):
            return str(obj)
        return super().default(obj)
 
 
def normalize_json_value(value, nan_replacement=None):
    """
    Recursively normalize values so JSON serialization works cleanly.
    Replace NaN / pd.NA / pd.NaT with nan_replacement (None => null).
    """
    if isinstance(value, dict):
        return {k: normalize_json_value(v, nan_replacement) for k, v in value.items()}

    if isinstance(value, (list, tuple, set)):
        return [normalize_json_value(v, nan_replacement) for v in value]

    if isinstance(value, np.ndarray):
        return normalize_json_value(value.tolist(), nan_replacement)

    if isinstance(value, pd.Series):
        return normalize_json_value(value.to_dict(), nan_replacement)

    if isinstance(value, pd.DataFrame):
        return normalize_json_value(value.to_dict(orient="records"), nan_replacement)

    if isinstance(value, (np.generic,)):
        return value.item()

    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()

    if isinstance(value, (np.dtype, ExtensionDtype)):
        return str(value)

    if pd.isna(value):
        return nan_replacement

    return value


def to_json(data: dict, indent=2, nan_replacement=None) -> str:
    """Convert data to JSON string using the custom encoder."""
    normalized = normalize_json_value(data, nan_replacement=nan_replacement)
    return json.dumps(normalized, cls=NumpyPandasEncoder, indent=indent, allow_nan=False)

