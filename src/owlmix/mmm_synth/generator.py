import pandas as pd
from os import PathLike
from collections.abc import Mapping
from pathlib import Path
from typing import Any
 
from .config.loader import ConfigLoader
from .core.time_builder import TimeSeriesBuilder
from .core.media_simulator import MediaChannelSimulator
from .core.drivers import BusinessDriverSimulator
from .core.transformations import TransformationEngine
from .core.sales import SalesAssembler
from .core.collinearity import CollinearityConfig, MulticollinearityInjector
from .core.target_assembler import TargetAssembler
from .core.time_builder import TimeSeriesBuilder
from .core.media_simulator import MediaChannelSimulator
from .core.target_assembler import TargetAssembler


class MMMDataGenerator:
 
    def __init__(self, config: Mapping[str, Any] | str | PathLike[str]):
        """
        Initializes the MMMDataGenerator with the provided configuration, which 
        can be either a mapping or a file path to a YAML configuration file.
        """
        self.config = self._coerce_config(config)
        self.time_builder = TimeSeriesBuilder(self.config)
        self.media_simulator = MediaChannelSimulator(self.config["media_channels"])
        self.target_assembler = TargetAssembler(self.config)
        self._normalize_config(self.config)
        self.media_channels = self._get_media_channels()

    def _coerce_config(self, config: Mapping[str, Any] | str | PathLike[str]) -> dict[str, Any]:
        """
        Coerces the input configuration into a standardized dictionary format, 
        ensuring that all necessary keys are present and correctly formatted.
        """
        match config:
            case Mapping():
                return dict(config)
            case str():
                return ConfigLoader(config).config
            case PathLike():
                return ConfigLoader(Path(config)).config
            case _:
                raise TypeError(
                    "Config must be a mapping or a filesystem path (str/PathLike)"
                )

    def _normalize_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """
        Ensures backward compatibility across:
        - media_channel
        - media_channels
        - channel
        """
 
        if not isinstance(config, dict):
            raise TypeError("Config must be a dictionary")
 
        # ---- media channels naming ----
        if "media_channels" not in config:
            if "media_channel" in config:
                config["media_channels"] = config["media_channel"]
            elif "channel" in config:
                config["media_channels"] = config["channel"]
 
        # ---- ensure list ----
        if isinstance(config.get("media_channels"), str):
            config["media_channels"] = [config["media_channels"]]
 
        if not config.get("media_channels"):
            raise ValueError("Missing media channels configuration")
 
        # ---- channel_coefs default ----
        if "channel_coefs" not in config:
            config["channel_coefs"] = {
                ch: 1.0 for ch in config["media_channels"]
            }
 
        # ---- dataset defaults (avoid earlier crashes) ----
        dataset = config.get("dataset", {})
 
        dataset.setdefault("start_date", "2020-01-01")
        dataset.setdefault("periods", 100)
        dataset.setdefault("freq", "D")
 
        config["dataset"] = dataset
 
        return config
 
    def _get_media_channels(self) -> list[str]:
    
        possible_keys = ["media_channels", "media_channel", "channels", "channel"]
    
        for key in possible_keys:
            if key in self.config:
                channels = self.config[key]
    
                if not isinstance(channels, list) or len(channels) == 0:
                    raise ValueError(f"'{key}' must be a non-empty list")
    
                print(f"[DEBUG] Using '{key}' for media channels")
                return channels
    
        # If nothing found — show actual config keys
        raise ValueError(
            f"Missing media channels configuration.\n"
            f"Expected one of {possible_keys}\n"
            f"Available keys: {list(self.config.keys())}"
        )
 
    def generate(self):
 
        # 1. Build time index
        time_df = self.time_builder.build()
 
        # 2. Simulate media
        media_df = self.media_simulator.simulate(n=len(time_df))
 
        # 3. Merge
        df = time_df.merge(media_df, left_index=True, right_index=True)
 
        # 4. Apply correlations (if any)
        df = self._apply_correlations(df)
 
        # 5. Build target
        df = self.target_assembler.assemble(df)
 
        return df

    # 🔗 Correlation handler
    def _apply_correlations(self, df: pd.DataFrame) -> pd.DataFrame:
        correlations = self.config.get("channel_correlations", [])

        if not correlations:
            return df

        sanitized = self._validate_and_prepare_correlations(correlations, df.columns)

        if not sanitized:
            return df

        injector = MulticollinearityInjector(
            n=len(df),
            collinearity_config=sanitized,
        )
        return injector.apply(df)

    def _validate_and_prepare_correlations(self, correlations: Any, columns: pd.Index) -> list[CollinearityConfig]:
        if not isinstance(correlations, list):
            raise ValueError("channel_correlations must be a list")

        sanitized: list[CollinearityConfig] = []
        for i, cfg in enumerate(correlations):
            if not isinstance(cfg, Mapping):
                raise ValueError(
                    f"Invalid correlation config at index {i}: expected dict"
                )

            channels = cfg.get("channels", [])
            if not isinstance(channels, list) or len(channels) < 2:
                raise ValueError(
                    f"Correlation must include at least 2 channels (index {i})"
                )

            present_channels = [ch for ch in channels if ch in columns]
            if len(present_channels) < 2:
                continue

            strength = cfg.get("correlation", cfg.get("collinearity", None))
            if strength is None:
                raise ValueError(
                    f"Invalid correlation config at index {i}: missing 'correlation'"
                )

            sanitized.append(
                {
                    "channels": present_channels,
                    "correlation": float(strength),
                }
            )

        return sanitized
 
 