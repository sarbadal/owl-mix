import pandas as pd
import numpy as np
from typing import TypedDict, NotRequired


class CollinearityConfig(TypedDict):
    channels: list[str]
    collinearity: float
 
 
class MulticollinearityInjector:
    """
    Injects multicollinearity into synthetic media channel data 
    based on specified configurations.
    Args:
        n (int): Number of data points.
        collinearity_config (list[CollinearityConfig]): Configuration list for multicollinearity settings.
    """
    def __init__(self, n: int, collinearity_config: list[CollinearityConfig]):
        self.n = n
        self.collinearity_config = collinearity_config
 
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies multicollinearity to the media channel data in the DataFrame 
        based on the specified configuration.
        Args:
            df (pd.DataFrame): 
                DataFrame containing media channel data 
                to which multicollinearity will be applied.
        Returns:
            pd.DataFrame: 
                DataFrame with multicollinearity applied to specified media channels.
        """
        if not self.collinearity_config:
            return df
 
        df = df.copy()
        for cfg in self.collinearity_config:
            latent = np.random.normal(0, 1, self.n)
            strength = cfg["correlation"]
 
            for ch in cfg["channels"]:
                if ch in df.columns:
                    df[ch] += strength * latent * np.std(df[ch])
 
        return df