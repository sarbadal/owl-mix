import pandas as pd
 
 
def cleanup_data(df: pd.DataFrame, drop_na: bool = True, reset_index: bool = True) -> pd.DataFrame:
    """
    Final cleanup after transformations.
 
    Parameters:
    ----------
    df : pd.DataFrame
        Input dataframe
    drop_na : bool
        Whether to drop rows with NaN values
    reset_index : bool
        Whether to reset index after cleaning
 
    Returns:
    -------
    pd.DataFrame
    """
 
    df = df.copy()
 
    if drop_na:
        df = df.dropna()
 
    if reset_index:
        df = df.reset_index(drop=True)
 
    return df