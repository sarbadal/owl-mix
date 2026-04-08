"""
Saturation transformation for diminishing returns in media mix modeling.

In Marketing mix modeling, saturation transformations are used to capture the 
diminishing returns of marketing spend. This module provides a Hill-type 
saturation function and a helper to apply it to DataFrame columns.
"""
import pandas as pd
import numpy as np
 
 
def hill_saturation(series: pd.Series, alpha: float = 1.0, gamma: float = 1.0) -> pd.Series:
    """
    Apply Hill-type saturation (diminishing returns).
 
    Parameters:
    ----------
    series : pd.Series
        Input variable (e.g., ad spend)
    alpha : float
        Controls curve steepness
    gamma : float
        Half-saturation point (inflection)
 
    Returns:
    -------
    pd.Series
        Saturated values
    """
    if alpha <= 0:
        raise ValueError("alpha must be > 0")
    if gamma <= 0:
        raise ValueError("gamma must be > 0")
 
    return (series ** alpha) / (series ** alpha + gamma ** alpha)


def log_saturation(series: pd.Series, alpha: float = 1.0) -> pd.Series:
    """
    Apply logarithmic saturation.
 
    Parameters:
    ----------
    series : pd.Series
        Input variable (e.g., ad spend)
    alpha : float
        Controls curve steepness
 
    Returns:
    -------
    pd.Series
        Saturated values
    """
    if alpha <= 0:
        raise ValueError("alpha must be > 0")
 
    return np.log1p(series * alpha)


def exp_saturation(series: pd.Series, lam: float = 0.01) -> pd.Series:
    """
    Apply exponential saturation.
 
    Parameters:
    ----------
    series : pd.Series
        Input variable (e.g., ad spend)
    lam : float
        Controls curve steepness
 
    Returns:
    -------
    pd.Series
        Saturated values
    """
    if lam <= 0:
        raise ValueError("lam must be > 0")
 
    return 1 - np.exp(-series * lam)


def saturation(series: pd.Series, method: str = "hill", alpha: float = 1.0, gamma: float = 1.0, lam: float = 0.01) -> pd.Series:
    """
    Apply saturation transformation.
 
    Parameters:
    ----------
    series : pd.Series
    method : str
        "hill", "log", "exp"
    alpha : float
        Hill parameter
    gamma : float
        Hill parameter
    lam : float
        Exponential parameter
 
    Returns:
    -------
    pd.Series
    """
 
    if method == "hill":
        if alpha <= 0 or gamma <= 0:
            raise ValueError("alpha and gamma must be > 0")
        return (series ** alpha) / (series ** alpha + gamma ** alpha)
 
    elif method == "log":
        return np.log1p(series)
 
    elif method == "exp":
        if lam <= 0:
            raise ValueError("lam must be > 0")
        return 1 - np.exp(-lam * series)
 
    else:
        raise ValueError(f"Unknown method: {method}")


def apply_saturation(df: pd.DataFrame, column: str, method: str = "hill", new_column: str | None = None, **kwargs) -> pd.DataFrame:
    """Apply saturation to a DataFrame column."""
 
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")
 
    if new_column is None:
        new_column = f"{column}_{method}_sat"
 
    df = df.copy()
    df[new_column] = saturation(df[column], method=method, **kwargs)
 
    return df