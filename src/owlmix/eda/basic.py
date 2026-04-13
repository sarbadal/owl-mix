# src/owlmix/eda/basic.py
import json
import pandas as pd

from .utils import to_json

def get_basic_info(df: pd.DataFrame):
    """Get basic info about the DataFrame."""
    shape = df.shape
    columns = df.columns.tolist()
    dtypes = df.dtypes.to_dict()
    missing = df.isnull().sum().to_dict()
    summary = df.describe().to_dict()

    info = {}
    info["num_rows"] = shape[0]
    info["num_columns"] = shape[1]
    info["column_names"] = columns
    info["data_types"] = dtypes
    info["missing_values"] = missing
    info["summary_stats"] = summary
    json_content = result_df.to_json()
    return json_content


class BasicInfo:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.result = None

    def compute(self) -> dict:
        """Compute basic info about the DataFrame."""
        shape = self.df.shape
        columns = self.df.columns.tolist()
        dtypes = self.df.dtypes.to_dict()
        missing = self.df.isnull().sum().to_dict()
        summary = self.df.describe().to_dict()

        result = {
            "num_rows": shape[0],
            "num_columns": shape[1],
            "column_names": columns,
            "data_types": dtypes,
            "missing_values": missing,
            "summary_stats": summary
        }
        self.result = result
        # print(result)
        return result

    def to_json(self) -> str:
        """Get the basic info as a JSON string."""
        if self.result is None:
            self.compute()
        json_str = to_json(self.result)
        return json_str
