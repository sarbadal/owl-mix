import numpy as np
import pandas as pd
from typing import TypedDict, NotRequired


class MediaChannelParams(TypedDict, total=False):
    shape: NotRequired[float]
    scale: NotRequired[float]
    clip_min: NotRequired[float]
    zero_fraction: NotRequired[float]



class MediaChannelConfig(TypedDict):
    """
    Configuration for a media channel, including distribution type and parameters.
    Args:
        name (str): Name of the media channel.
        type (str): Type of the media channel.
        distribution (str): Type of distribution to use for generating data (e.g., "gamma", "normal").
        params (MediaChannelParams): Parameters for the specified distribution.
    """
    name: str
    type: str
    distribution: str
    params: MediaChannelParams
 
 
class MediaChannelSimulator:
    """
    Simulates synthetic media channel data based on specified configurations.
    Args:
        n (int): Number of data points to generate.
        channel_config (dict): Configuration dictionary for each media channel.
    """
    VALID_DISTRIBUTIONS = ["gamma", "normal", "lognormal"]

    def __init__(self, channel_config: list[MediaChannelConfig]):
        self.channel_config = channel_config
 
    def _generate(self, cfg: MediaChannelConfig, n: int) -> np.ndarray:
        """
        Generates synthetic media channel data based on the specified distribution and parameters.
        Args:
            cfg (MediaChannelConfig): Configuration for the media channel, including distribution type and parameters.
            n (int): Number of data points to generate.
        Returns:
            np.ndarray: Generated media channel data.
        Raises:
            ValueError: If the specified distribution is unsupported.
        """
        dist = cfg["distribution"]
        p = cfg["params"]

        if dist not in self.VALID_DISTRIBUTIONS:
            raise ValueError(f"Unsupported distribution: {dist}")
 
        if dist == "gamma":
            data = np.random.gamma(p["shape"], p["scale"], n)
        if dist == "normal":
            data = np.random.normal(p["mean"], p["std"], n)
        if dist == "lognormal":
            data = np.random.lognormal(p["mean"], p["sigma"], n)
 
        if "clip_min" in p:
            data = np.clip(data, p["clip_min"], None)
 
        if "zero_fraction" in cfg:
            idx = np.random.choice(n, int(cfg["zero_fraction"] * n), replace=False)
            data[idx] = 0
 
        return data
 
    def simulate(self, n: int) -> pd.DataFrame:
        """
        Simulates synthetic media channel data for all configured channels.
        Args:
            n (int): Number of data points to generate.
        Returns:
            pd.DataFrame: DataFrame containing simulated media channel data.
        """
        df = pd.DataFrame()
 
        for media_config in self.channel_config:
            df[media_config["name"]] = self._generate(media_config, n)
 
        return df