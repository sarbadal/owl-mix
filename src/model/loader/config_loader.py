import json
from pathlib import Path

from ..models.config_model import ConfigModel

def load_config(config_path: str | Path) -> ConfigModel:
    """Load the model configuration from a JSON file."""
    config_path = Path(config_path).resolve()
    with open(config_path, mode="r", encoding="utf-8") as f:
        config_data = json.load(f)
    return ConfigModel.model_validate(config_data)