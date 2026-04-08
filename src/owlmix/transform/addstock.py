import pandas as pd
 
 
def adstock(series: pd.Series, decay: float = 0.5) -> pd.Series:
    """
    Apply adstock transformation to a pandas Series.
 
    Parameters:
    ----------
    series : pd.Series
        Input time series (e.g., marketing spend)
    decay : float
        Decay rate between 0 and 1
 
    Returns:
    -------
    pd.Series
        Adstock-transformed series
    """
    if not (0 <= decay <= 1):
        raise ValueError("Decay rate must be between 0 and 1.")
        
    result = []
    prev = 0
 
    for value in series:
        current = value + decay * prev
        result.append(current)
        prev = current
 
    return pd.Series(result, index=series.index)
 
 
def apply_adstock(df: pd.DataFrame, column: str, decay: float = 0.5, new_column: str | None = None) -> pd.DataFrame:
    """
    Apply adstock transformation to a DataFrame column.
 
    Parameters:
    ----------
    df : pd.DataFrame
        Input dataframe
    column : str
        Column to transform
    decay : float
        Decay rate
    new_column : str, optional
        Name of output column
 
    Returns:
    -------
    pd.DataFrame
        DataFrame with adstock column added
    """
    if new_column is None:
        new_column = f"{column}_adstock"
 
    df[new_column] = adstock(df[column], decay)
    return df