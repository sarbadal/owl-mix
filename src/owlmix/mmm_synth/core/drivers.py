import numpy as np
import pandas as pd
 
 
class BusinessDriverSimulator:
    """
    Simulates business drivers such as promotions, pricing, and store coverage.
    Args:
        n (int): Number of data points to simulate.
        config (list): List of configuration dictionaries for business drivers.
    """
    def __init__(self, config: list[dict]):
        self.cfg = config
 
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

            if dist_type == "normal":
                df[column] = np.random.normal(cfg["mean"], cfg["std"], n) + latent
            if dist_type == "uniform":
                df[column] = np.random.uniform(cfg["low"], cfg["high"], n) + latent
            if dist_type == "binomial":
                df[column] = np.random.binomial(1, cfg["probability"], n) + latent
            if dist_type == "poisson":
                df[column] = np.random.poisson(cfg["lam"], n) + latent
            if dist_type == "exponential":
                df[column] = np.random.exponential(cfg["scale"], n) + latent
            if dist_type == "lognormal":
                df[column] = np.random.lognormal(cfg["mean"], cfg["sigma"], n) + latent
            if dist_type == "continuous":
                df[column] = np.clip(latent, cfg["clip_min"], None)
            if dist_type == "zero_inflated":
                zero_mask = np.random.rand(n) < cfg["zero_fraction"]
                df[column] = np.where(zero_mask, 0, latent)

        return df