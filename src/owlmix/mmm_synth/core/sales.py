import pandas as pd
import numpy as np
 
 
class SalesAssembler:
    """
    Assembles the total sales by combining baseline trend, seasonality,
    media channel effects, and business drivers.
    """
    def build(self, df: pd.DataFrame, config: dict) -> pd.Series:
        """
        Assembles the total sales by combining baseline trend, seasonality,
        media channel effects, and business drivers.
        Args:
            df (pd.DataFrame): DataFrame containing baseline trend, seasonality,
                               media channel effects, and business drivers.
            config (dict): Configuration dictionary containing beta coefficients
                           for media channels and business drivers, as well as
                           noise parameters.
        Returns:
            pd.Series: Series containing the assembled total sales.
        """
        sales = df["baseline_trend"] + df["seasonality"]
 
        for ch, cfg in config["channels"].items():
            sales += cfg["beta"] * df[cfg["effect_name"]]
 
        sales += config["drivers"]["promotion"]["beta"] * df["promotion_active"]
        sales += config["drivers"]["price"]["beta"] * df["price_per_unit"]
        sales += config["drivers"]["distribution"]["beta"] * df["store_coverage_pct"]
 
        sales += np.random.normal(0, config["noise"]["std"], len(df))
 
        return sales