import numpy as np
import pandas as pd
from typing import Callable, Literal, NotRequired, TypedDict


class MediaChannelParams(TypedDict, total=False):
    shape: NotRequired[float]
    scale: NotRequired[float]
    mean: NotRequired[float]
    std: NotRequired[float]
    sigma: NotRequired[float]
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
    distribution: Literal["gamma", "normal", "lognormal"]
    params: MediaChannelParams
    zero_fraction: NotRequired[float]


DistributionType = Literal["gamma", "normal", "lognormal"]
MediaDistributionGenerator = Callable[[MediaChannelParams, int], np.ndarray]
 
 
class MediaChannelSimulator:
    """
    Simulates synthetic media channel data based on specified configurations.
    Args:
        n (int): Number of data points to generate.
        channel_config (dict): Configuration dictionary for each media channel.
    """
    def __init__(self, channel_config: list[MediaChannelConfig]):
        self.channel_config = channel_config
        self.dist_generators: dict[DistributionType, MediaDistributionGenerator] = {
            "gamma": self._gen_gamma,
            "normal": self._gen_normal,
            "lognormal": self._gen_lognormal,
        }

    def _gen_gamma(self, params: MediaChannelParams, n: int) -> np.ndarray:
        return np.random.gamma(params["shape"], params["scale"], n)

    def _gen_normal(self, params: MediaChannelParams, n: int) -> np.ndarray:
        return np.random.normal(params["mean"], params["std"], n)

    def _gen_lognormal(self, params: MediaChannelParams, n: int) -> np.ndarray:
        return np.random.lognormal(params["mean"], params["sigma"], n)

    def _apply_post_processing(self, data: np.ndarray, params: MediaChannelParams, cfg: MediaChannelConfig, n: int) -> np.ndarray:
        if "clip_min" in params:
            data = np.clip(data, params["clip_min"], None)

        zero_fraction = params.get("zero_fraction", cfg.get("zero_fraction", 0.0))
        if zero_fraction > 0:
            idx = np.random.choice(n, int(zero_fraction * n), replace=False)
            data[idx] = 0

        return data
 
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
        params = cfg["params"]
        dist = cfg["distribution"]
        generator = self.dist_generators.get(dist)

        if generator is None:
            raise ValueError(f"Unsupported distribution: {dist}")

        data = generator(params, n)
        return self._apply_post_processing(data, params, cfg, n)
 
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