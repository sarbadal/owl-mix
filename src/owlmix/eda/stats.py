# src/owlmix/eda/stats.py
import json 
import pandas as pd

from .utils import to_json
 
 
def get_basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    summary = pd.DataFrame({
        "dtype": df.dtypes,
        "missing_count": df.isna().sum(),
        "missing_pct": df.isna().mean() * 100,
        "n_unique": df.nunique()
    })
 
    return json.dumps(summary, indent=2)


class BasicStats:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.result = None
 
    def compute(self) -> dict:
        description = self.df.describe(include="all")
        self.result = {
            "summary": description.fillna("").to_dict()
        }
        return self.result

    def to_json(self) -> str:
        if self.result is None:
            self.compute()
        return to_json(self.result)