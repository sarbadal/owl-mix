# src/owlmix/eda/charts/utils.py
import pandas as pd


def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include=["number"]).columns.tolist()