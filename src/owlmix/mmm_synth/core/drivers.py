import numpy as np
import pandas as pd
from typing import Callable, Literal, NotRequired, TypedDict


class BusinessDriverConfig(TypedDict, total=False):
    name: str
    type: Literal[
        "normal",
        "uniform",
        "binomial",
        "poisson",
        "exponential",
        "lognormal",
        "continuous",
        "zero_inflated",
    ]
    mean: NotRequired[float]
    std: NotRequired[float]
    low: NotRequired[float]
    high: NotRequired[float]
    probability: NotRequired[float]
    lam: NotRequired[float]
    scale: NotRequired[float]
    sigma: NotRequired[float]
    clip_min: NotRequired[float]
    zero_fraction: NotRequired[float]


DistributionGenerator = Callable[[BusinessDriverConfig, int, np.ndarray], np.ndarray]
 
 
class BusinessDriverSimulator:
    """
    Simulates business drivers such as promotions, pricing, and store coverage.
    Args:
        n (int): Number of data points to simulate.
        config (list): List of configuration dictionaries for business drivers.
    """
    def __init__(self, config: list[BusinessDriverConfig]):
        self.cfg = config
        self.dist_generators: dict[str, DistributionGenerator] = {
            "normal": self._gen_normal,
            "uniform": self._gen_uniform,
            "binomial": self._gen_binomial,
            "poisson": self._gen_poisson,
            "exponential": self._gen_exponential,
            "lognormal": self._gen_lognormal,
            "continuous": self._gen_continuous,
            "zero_inflated": self._gen_zero_inflated,
        }

    def _gen_normal(self, cfg: BusinessDriverConfig, n: int, latent: np.ndarray) -> np.ndarray:
        return np.random.normal(cfg["mean"], cfg["std"], n) + latent

    def _gen_uniform(self, cfg: BusinessDriverConfig, n: int, latent: np.ndarray) -> np.ndarray:
        return np.random.uniform(cfg["low"], cfg["high"], n) + latent

    def _gen_binomial(self, cfg: BusinessDriverConfig, n: int, latent: np.ndarray) -> np.ndarray:
        return np.random.binomial(1, cfg["probability"], n) + latent

    def _gen_poisson(self, cfg: BusinessDriverConfig, n: int, latent: np.ndarray) -> np.ndarray:
        return np.random.poisson(cfg["lam"], n) + latent

    def _gen_exponential(self, cfg: BusinessDriverConfig, n: int, latent: np.ndarray) -> np.ndarray:
        return np.random.exponential(cfg["scale"], n) + latent

    def _gen_lognormal(self, cfg: BusinessDriverConfig, n: int, latent: np.ndarray) -> np.ndarray:
        return np.random.lognormal(cfg["mean"], cfg["sigma"], n) + latent

    def _gen_continuous(self, cfg: BusinessDriverConfig, n: int, latent: np.ndarray) -> np.ndarray:
        return np.clip(latent, cfg["clip_min"], None)

    def _gen_zero_inflated(self, cfg: BusinessDriverConfig, n: int, latent: np.ndarray) -> np.ndarray:
        zero_mask = np.random.rand(n) < cfg["zero_fraction"]
        return np.where(zero_mask, 0, latent)
 
    def simulate(self, n: int) -> pd.DataFrame:
        """
        Simulates business drivers based on the configuration.
        Returns:
            pd.DataFrame: DataFrame containing simulated business drivers.
        """
        df = pd.DataFrame()

        for cfg in self.cfg:
            latent = np.random.normal(0, 1, n)
            column = cfg["name"]
            dist_type = cfg["type"]

            generator = self.dist_generators.get(dist_type)
            if generator is None:
                raise ValueError(f"Unsupported distribution type: {dist_type}")

            df[column] = generator(cfg, n, latent)

        return df