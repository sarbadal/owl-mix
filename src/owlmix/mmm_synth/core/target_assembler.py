import pandas as pd
import numpy as np
 
 
class TargetAssembler:
    """
    Responsible for generating the final target variable (e.g., sales)
    using latent transformations of media channels and control variables.
 
    IMPORTANT:
    - Effects are NOT exposed in final dataset (unless debug enabled)
    - Prevents data leakage
    """
 
    def __init__(self, config: dict):
        self.config = config
 
        self.base_sales = config.get("base_sales", 1000)
        self.noise_std = config.get("noise_std", 50)
 
        # channel coefficients (impact strength)
        self.channel_coefs = config.get("channel_coefs", {})
 
        # transformation configs
        self.transformations = config.get("transformations", {})

    def _generate_noise(self, size):
        noise_cfg = self.config.get("noise", {"type": "gaussian", "std": 50})
    
        if noise_cfg["type"] == "gaussian":
            return np.random.normal(0, noise_cfg.get("std", 50), size)
    
        if noise_cfg["type"] == "lognormal":
            return np.random.lognormal(0, noise_cfg.get("sigma", 0.3), size)
    
        if noise_cfg["type"] == "laplace":
            return np.random.laplace(0, noise_cfg.get("scale", 50), size)
    
        return np.zeros(size)
 
    # --------------------------------------------------
    # Public API
    # --------------------------------------------------
    def assemble(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main method to generate target variable.
        Args:
            df: DataFrame containing media channels and control variables.
        Returns:
            DataFrame with target variable added.
        """
        latent_effects = {}
 
        # Step 1: compute latent effects
        for channel in self.channel_coefs.keys():
            if channel not in df.columns:
                continue
 
            raw_values = df[channel].values
            effect = self._apply_transform(channel, raw_values)
 
            latent_effects[channel] = effect
 
        # Step 2: combine effects into sales
        sales = np.full(len(df), self.base_sales, dtype=float)
 
        for channel, effect in latent_effects.items():
            coef = self.channel_coefs.get(channel, 1.0)
            if isinstance(coef, dict):
                coef = coef.get("coefficient", 1.0)
            else:
                coef = float(coef)
            sales += coef * effect
 
        # Step 3: add noise
        noise = self._generate_noise(size=len(df))
        sales += noise
 
        # Step 4: attach target
        df["weekly_sales_units"] = np.maximum(sales, 0)  # avoid negative sales
 
        # Step 5 (optional): debug mode
        if self.config.get("include_latent_effects", False):
            for k, v in latent_effects.items():
                df[f"{k}_effect"] = v
 
        return df
 
    # --------------------------------------------------
    # Internal helpers
    # --------------------------------------------------
    def _apply_transform(self, channel: str, x: np.ndarray) -> np.ndarray:
        """
        Applies transformation like adstock + saturation.
        Args:
            channel: Name of the channel.
            x: Array of channel values.
        Returns:
            Transformed array.
        """
        config = self.transformations.get(channel, {})
        if not config:
            coef_cfg = self.channel_coefs.get(channel, {})
            if isinstance(coef_cfg, dict):
                config = {
                    "adstock": coef_cfg.get("adstock", 0.0),
                    "saturation": coef_cfg.get("saturation", None)
                }
 
        # Adstock
        adstock_rate = config.get("adstock", 0.0)
        x_adstock = self._adstock(x, adstock_rate)
 
        # Saturation (diminishing returns)
        saturation = config.get("saturation", None)
        if saturation:
            x_sat = self._saturation(x_adstock, saturation)
        else:
            x_sat = x_adstock
 
        return x_sat
 
    def _adstock(self, x, rate):
        """
        Simple geometric adstock.
        Args:
            x: Array of channel values.
            rate: Adstock rate.
        Returns:
            Transformed array.
        """
        if rate <= 0:
            return x
 
        result = np.zeros_like(x)
        result[0] = x[0]
 
        for t in range(1, len(x)):
            result[t] = x[t] + rate * result[t - 1]
 
        return result
 
    def _saturation(self, x, sat_type):
        """
        Applies saturation curve.
        Args:
            x: Array of channel values.
            sat_type: Type of saturation curve ("log", "sqrt", "hill").
        Returns:
            Transformed array.
        """
        if sat_type == "log":
            return np.log1p(x)
 
        if sat_type == "sqrt":
            return np.sqrt(x)
 
        if sat_type == "hill":
            alpha = self.config.get("hill_alpha", 1.0)
            return (x ** alpha) / (1 + x ** alpha)
        
        return x