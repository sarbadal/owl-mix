# owlmix/eda/utils.py
import json
from datetime import datetime
from typing import Any, List, Optional, Dict

import numpy as np
import pandas as pd
from pandas.core.dtypes.base import ExtensionDtype


class CategoricalColumnMixin:
    """Mixin to extract categorical columns from a DataFrame."""
    def _get_columns(self, columns: Optional[List[str]] = None) -> List[str]:
        if columns:
            valid_columns = [col for col in self.df.columns if col in columns]
            if not valid_columns:
                raise ValueError("None of the specified columns are present in the DataFrame.")
            return valid_columns
        return self.df.select_dtypes(include=["object", "category"]).columns.tolist()


class ColumnMixin:
    """Mixin to extract numeric columns from a DataFrame."""
    def _get_columns(self, value_columns: Optional[List[str]] = None) -> List[str]:
        if value_columns:
            valid_columns = [col for col in self.df.columns if col in value_columns]
            if not valid_columns:
                raise ValueError("None of the specified columns are present in the DataFrame.")
            numeric_cols = self.df[valid_columns].select_dtypes(include=["number"]).columns.tolist()
            if not numeric_cols:
                raise ValueError("None of the provided columns are numeric.")
            return numeric_cols
        return self.df.select_dtypes(include=["number"]).columns.tolist()


class SerializableMixin:
    """Mixin to serialize DataFrame to a JSON-serializable structure."""
    def _to_serializable(self) -> Dict[str, Any]:
        return {
            "columns": self.value_columns,
            "data": [
                {k: self._safe(v) for k, v in row.items()}
                for _, row in self.df.iterrows()
            ]
        }

    def _safe(self, val: Any) -> Any:
        if pd.isna(val):
            return None
        if isinstance(val, (int, float)):
            rounded = round(float(val), self.precision)
            return int(rounded) if rounded.is_integer() else rounded
        return str(val).split(" ")[0]


class NumpyPandasEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle numpy and pandas data types."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (pd.Timestamp, datetime)):
            return obj.isoformat()
        if isinstance(obj, pd.Series):
            return obj.to_dict()
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient="records")
        if isinstance(obj, (np.dtype, ExtensionDtype)):
            return str(obj)
        return super().default(obj)


def normalize_json_value(value: Any, nan_replacement: Any = None) -> Any:
    """
    Recursively normalize values for JSON serialization.
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
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if isinstance(value, (np.dtype, ExtensionDtype)):
        return str(value)
    if pd.isna(value):
        return nan_replacement
    return value


def to_json(data: dict, indent: int = 2, nan_replacement: Any = None) -> str:
    """Convert data to JSON string using the custom encoder."""
    normalized = normalize_json_value(data, nan_replacement=nan_replacement)
    return json.dumps(normalized, cls=NumpyPandasEncoder, indent=indent, allow_nan=False)

