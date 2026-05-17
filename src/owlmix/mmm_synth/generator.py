import numpy as np
import pandas as pd
 
from .config.loader import ConfigLoader
from .core.time_builder import TimeSeriesBuilder
from .core.media_simulator import MediaChannelSimulator
from .core.drivers import BusinessDriverSimulator
from .core.transformations import TransformationEngine
from .core.sales import SalesAssembler
from .core.collinearity import MulticollinearityInjector
from .core.target_assembler import TargetAssembler
from .core.time_builder import TimeSeriesBuilder
from .core.media_simulator import MediaChannelSimulator
from .core.target_assembler import TargetAssembler
 
 
class MMMDataGenerator_OLD:
    def __init__(self, config_path):
        self.config = ConfigLoader.load(config_path)
        np.random.seed(self.config.get("seed", 42))
 
    def generate(self):
        time_df = TimeSeriesBuilder(self.config).build()
 
        media_df = MediaChannelSimulator(
            len(time_df),
            self.config["channels"]
        ).simulate()
 
        media_df = MulticollinearityInjector(
            len(time_df),
            self.config["channels"],
            self.config.get("collinearity", {})
        ).apply(media_df)
 
        drivers_df = BusinessDriverSimulator(
            len(time_df),
            self.config
        ).simulate()
 
        df = pd.concat([time_df, media_df, drivers_df], axis=1)
 
        effects_df = TransformationEngine().apply(df, self.config["channels"])
        df = pd.concat([df, effects_df], axis=1)
 
        df["total_sales"] = TargetAssembler(self.config).assemble(df)
 
        return df.drop(columns=["time_index"])


class MMMDataGenerator:
 
    def __init__(self, config: dict):
 
        # ✅ Accept BOTH:
        # - dict (already loaded)
        # - string (path to YAML)
 
        if isinstance(config, str):
            self.config = ConfigLoader.load(config)
 
        elif isinstance(config, dict):
            self.config = config
 
        else:
            raise ValueError(
                "config must be either a dict or a file path string"
            )

        self.time_builder = TimeSeriesBuilder(self.config)
        self.media_simulator = MediaChannelSimulator(self.config)
        self.target_assembler = TargetAssembler(self.config)
 
        # Optional but recommended
        self._normalize_config(self.config)
 
        # Now safe
        self.media_channels = self._get_media_channels()

    def _normalize_config(self, config: dict) -> dict:
        """
        Ensures backward compatibility across:
        - media_channel
        - media_channels
        - channel
        """
 
        if not isinstance(config, dict):
            raise TypeError("Config must be a dictionary")
 
        # ---- FIX 1: media channels naming ----
        if "media_channels" not in config:
            if "media_channel" in config:
                config["media_channels"] = config["media_channel"]
            elif "channel" in config:
                config["media_channels"] = config["channel"]
 
        # ---- FIX 2: ensure list ----
        if isinstance(config.get("media_channels"), str):
            config["media_channels"] = [config["media_channels"]]
 
        if not config.get("media_channels"):
            raise ValueError("Missing media channels configuration")
 
        # ---- FIX 3: channel_coefs default ----
        if "channel_coefs" not in config:
            config["channel_coefs"] = {
                ch: 1.0 for ch in config["media_channels"]
            }
 
        # ---- FIX 4: dataset defaults (avoid earlier crashes) ----
        dataset = config.get("dataset", {})
 
        dataset.setdefault("start_date", "2020-01-01")
        dataset.setdefault("periods", 100)
        dataset.setdefault("freq", "D")
 
        config["dataset"] = dataset
 
        return config
 
    # --------------------------------------------------
    # 🧠 Handle old + new schema
    # --------------------------------------------------
    def _get_media_channels(self):
    
        possible_keys = ["media_channels", "media_channel", "channels", "channel"]
    
        for key in possible_keys:
            if key in self.config:
                channels = self.config[key]
    
                if not isinstance(channels, list) or len(channels) == 0:
                    raise ValueError(f"'{key}' must be a non-empty list")
    
                print(f"[DEBUG] Using '{key}' for media channels")
                return channels
    
        # 🔴 If nothing found — show actual config keys
        raise ValueError(
            f"Missing media channels configuration.\n"
            f"Expected one of {possible_keys}\n"
            f"Available keys: {list(self.config.keys())}"
        )
 
    # --------------------------------------------------
    # 🚀 MAIN GENERATION FLOW (example structure)
    # --------------------------------------------------
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
 
    # --------------------------------------------------
    # 🔗 OPTIONAL: Correlation handler
    # --------------------------------------------------
    def _apply_correlations(self, df):
 
        correlations = self.config.get("channel_correlations", [])
 
        # (keep your existing logic here)
        return df
 
 