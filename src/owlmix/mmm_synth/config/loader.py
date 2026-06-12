import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Utility class to load and validate configuration for MMM data synthesis."""

    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self.config = self.load(config_path)

    def load(self, path: str | Path | None = None) -> dict:
        path = self.config_path if path is None else Path(path)
        with open(path, mode="r") as f:
            config = yaml.safe_load(f)
        self._validate_config(config)
        return config

    def _validate_config(self, config: dict):
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")

        required_sections = [
            "dataset",
            "target",
            "media_channels",
            "channel_coefs"
        ]
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required config section: {section}")

        self._validate_dataset(config["dataset"])
        self._validate_target(config["target"])
        self._validate_media_channels(config["media_channels"])
        self._validate_channel_coefs(
            config["channel_coefs"],
            config["media_channels"]
        )

        if "channel_correlations" in config:
            self._validate_correlations(config["channel_correlations"])
        if "external_factors" in config:
            self._validate_external_factors(config["external_factors"])
        if "noise" in config:
            self._validate_noise(config["noise"])
        if "seed" in config:
            if not isinstance(config["seed"], int):
                raise ValueError("seed must be an integer")

    def _validate_dataset(self, dataset: dict):
        required_keys = ["start_date", "end_date", "frequency"]
        for key in required_keys:
            if key not in dataset:
                raise ValueError(f"Missing dataset field: {key}")
        if dataset["frequency"] not in ["daily", "weekly", "monthly"]:
            raise ValueError("frequency must be one of: daily, weekly, monthly")

    def _validate_target(self, target: dict):
        required_keys = ["name", "base_level"]
        for key in required_keys:
            if key not in target:
                raise ValueError(f"Missing target field: {key}")

    def _validate_media_channels(self, media_channels: list):
        if not isinstance(media_channels, list) or len(media_channels) == 0:
            raise ValueError("media_channels must be a non-empty list")
        required_keys = ["name", "distribution"]
        for i, channel in enumerate(media_channels):
            if not isinstance(channel, dict):
                raise ValueError(f"Each media channel must be a dict (index {i})")
            for key in required_keys:
                if key not in channel:
                    raise ValueError(
                        f"Missing '{key}' in media_channels[{i}]"
                    )

    def _validate_channel_coefs(self, channel_coefs: dict, media_channels: list):
        if not isinstance(channel_coefs, dict):
            raise ValueError("channel_coefs must be a dictionary")
        channel_names = [ch["name"] for ch in media_channels]
        for name in channel_names:
            if name not in channel_coefs:
                raise ValueError(
                    f"Missing coefficient config for channel: {name}"
                )
            coef = channel_coefs[name]
            if "coefficient" not in coef:
                raise ValueError(f"Missing coefficient for channel: {name}")
            if "adstock" in coef and not (0 <= coef["adstock"] <= 1):
                raise ValueError(f"Adstock must be between 0 and 1: {name}")
            if "saturation" in coef and not (0 <= coef["saturation"] <= 1):
                raise ValueError(f"Saturation must be between 0 and 1: {name}")

    def _validate_correlations(self, correlations: list):
        if not isinstance(correlations, list):
            raise ValueError("channel_correlations must be a list")
        for i, corr in enumerate(correlations):
            if "channels" not in corr or "correlation" not in corr:
                raise ValueError(
                    f"Invalid correlation config at index {i}"
                )
            if not isinstance(corr["channels"], list) or len(corr["channels"]) < 2:
                raise ValueError(
                    f"Correlation must include at least 2 channels (index {i})"
                )

    def _validate_external_factors(self, factors: list):
        if not isinstance(factors, list):
            raise ValueError("external_factors must be a list")
        for i, factor in enumerate(factors):
            if "name" not in factor:
                raise ValueError(f"Missing name in external_factors[{i}]")

    def _validate_noise(self, noise: dict):
        if "type" not in noise:
            raise ValueError("noise must include 'type'")
        if noise["type"] == "gaussian":
            if "std" not in noise:
                raise ValueError("Gaussian noise must include 'std'")