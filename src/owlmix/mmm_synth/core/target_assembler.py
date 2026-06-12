import pandas as pd
import numpy as np
from typing import Callable
 
 
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

        self.noise_generators: dict[str, Callable[[dict, int], np.ndarray]] = {
            "gaussian": self._noise_gaussian,
            "lognormal": self._noise_lognormal,
            "laplace": self._noise_laplace,
        }
        self.saturation_transforms: dict[str, Callable[[np.ndarray], np.ndarray]] = {
            "log": self._saturation_log,
            "sqrt": self._saturation_sqrt,
            "hill": self._saturation_hill,
        }

    def _noise_gaussian(self, noise_cfg: dict, size: int) -> np.ndarray:
        return np.random.normal(0, noise_cfg.get("std", 50), size)

    def _noise_lognormal(self, noise_cfg: dict, size: int) -> np.ndarray:
        return np.random.lognormal(0, noise_cfg.get("sigma", 0.3), size)

    def _noise_laplace(self, noise_cfg: dict, size: int) -> np.ndarray:
        return np.random.laplace(0, noise_cfg.get("scale", 50), size)

    def _generate_noise(self, size: int) -> np.ndarray:
        noise_cfg = self.config.get("noise", {"type": "gaussian", "std": 50})
        noise_type = noise_cfg.get("type", "gaussian")
        generator = self.noise_generators.get(noise_type)
        if generator is None:
            return np.zeros(size)

        return generator(noise_cfg, size)

    def _saturation_log(self, x: np.ndarray) -> np.ndarray:
        return np.log1p(x)

    def _saturation_sqrt(self, x: np.ndarray) -> np.ndarray:
        return np.sqrt(x)

    def _saturation_hill(self, x: np.ndarray) -> np.ndarray:
        alpha = self.config.get("hill_alpha", 1.0)
        return (x ** alpha) / (1 + x ** alpha)

    def _apply_saturation(self, x: np.ndarray, sat_type: str | None) -> np.ndarray:
        if not sat_type:
            return x

        saturation_fn = self.saturation_transforms.get(sat_type)
        if saturation_fn is None:
            return x

        return saturation_fn(x)

    def _extract_transform_config(self, channel: str) -> dict:
        config = self.transformations.get(channel, {})
        if config:
            return config

        coef_cfg = self.channel_coefs.get(channel, {})
        if isinstance(coef_cfg, dict):
            return {
                "adstock": coef_cfg.get("adstock", 0.0),
                "saturation": coef_cfg.get("saturation", None),
            }

        return {}

    def _coefficient_value(self, channel: str) -> float:
        coef = self.channel_coefs.get(channel, 1.0)
        if isinstance(coef, dict):
            return float(coef.get("coefficient", 1.0))

        return float(coef)

    def _adstock(self, x: np.ndarray, rate: float) -> np.ndarray:
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

    def _saturation(self, x: np.ndarray, sat_type: str | None) -> np.ndarray:
        """
        Applies saturation curve.
        Args:
            x: Array of channel values.
            sat_type: Type of saturation curve ("log", "sqrt", "hill").
        Returns:
            Transformed array.
        """
        return self._apply_saturation(x, sat_type)

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
            coef = self._coefficient_value(channel)
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
        config = self._extract_transform_config(channel)
 
        # Adstock
        adstock_rate = config.get("adstock", 0.0)
        x_adstock = self._adstock(x, adstock_rate)
 
        # Saturation (diminishing returns)
        saturation = config.get("saturation", None)
        x_sat = self._saturation(x_adstock, saturation)
 
        return x_sat