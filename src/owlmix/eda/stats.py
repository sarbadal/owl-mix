# src/owlmix/eda/stats.py
 
import pandas as pd
 
 
def get_basic_stats(df: pd.DataFrame) -> pd.DataFrame:
    summary = pd.DataFrame({
        "dtype": df.dtypes,
        "missing_count": df.isna().sum(),
        "missing_pct": df.isna().mean() * 100,
        "n_unique": df.nunique()
    })
 
    return summary