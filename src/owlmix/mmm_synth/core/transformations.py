import numpy as np
import pandas as pd
 
 
class TransformationEngine:
    """
    Applies specified transformations (e.g., adstock, saturation) to the 
    media channel data in the DataFrame.
    """
    @staticmethod
    def adstock(x: np.ndarray, decay: float) -> np.ndarray:
        """
        Applies adstock transformation to the input array.
        Args:
            x (np.ndarray): Input array.
            decay (float): Decay factor for adstock transformation.
        Returns:
            np.ndarray: Transformed array.
        """
        result = np.zeros_like(x)
        for i in range(len(x)):
            result[i] = x[i] + (result[i-1] * decay if i > 0 else 0)
        return result
 
    @staticmethod
    def saturation(x: np.ndarray, alpha: float = 1.5, gamma: float = 0.5) -> np.ndarray:
        """
        Applies saturation transformation to the input array.
        Args:
            x (np.ndarray): Input array.
            alpha (float): Alpha parameter for saturation transformation.
            gamma (float): Gamma parameter for saturation transformation.
        Returns:
            np.ndarray: Transformed array.
        """
        return (x**alpha) / (x**alpha + gamma**alpha)
 
    def apply(self, df: pd.DataFrame, channel_config: dict) -> pd.DataFrame:
        """
        Applies specified transformations to the media channel data in the DataFrame.
        Args:
            df (pd.DataFrame): DataFrame containing media channel data.
            channel_config (dict): Configuration dictionary for each media channel.
        Returns:
            pd.DataFrame: DataFrame with transformed media channel data.
        """
        effects = pd.DataFrame()
 
        for ch, cfg in channel_config.items():
            ad = self.adstock(df[ch].values, cfg["decay"])
            sat = self.saturation(ad)
 
            effects[cfg["effect_name"]] = sat
 
        return effects