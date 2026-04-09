# src/owlmix/eda/correlation.py
 
import pandas as pd
 
 
def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    return df.corr(numeric_only=True)
 
 
def get_lag_correlation(df: pd.DataFrame, column: str, target: str, lags: list[int]):
    results = {}
 
    for lag in lags:
        lagged = df[column].shift(lag)
        corr = lagged.corr(df[target])
        results[lag] = corr
 
    return pd.Series(results, name=f"{column}_lag_corr")