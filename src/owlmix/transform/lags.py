import pandas as pd
 
 
def create_lags(df: pd.DataFrame, columns: str | list[str], lags: int | list[int] = 1, drop_na: bool = False) -> pd.DataFrame:
    """
    Create lagged features for given columns.
 
    Parameters:
    ----------
    df : pd.DataFrame
        Input dataframe
    columns : str or list of str
        Column(s) to lag
    lags : int or list of int
        Lag period(s), e.g., 1 or [1, 2, 3]
        Default is 1 (lag of 1 period)
    drop_na : bool
        Whether to drop rows with NaN values after lagging
 
    Returns:
    -------
    pd.DataFrame
        DataFrame with lagged columns added
    """
 
    if isinstance(columns, str):
        columns = [columns]
 
    if isinstance(lags, int):
        lags = [lags]
 
    df = df.copy()
 
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")
 
        for lag in lags:
            if lag <= 0:
                raise ValueError("Lag must be a positive integer")
 
            new_col = f"{col}_lag{lag}"
            df[new_col] = df[col].shift(lag)
 
    if drop_na:
        df = df.dropna()
 
    return df