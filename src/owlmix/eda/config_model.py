from dataclasses import dataclass
from typing import Mapping, Union
from pathlib import Path
import json

from .summary_builder_config import SummaryBuilderConfig


@dataclass(frozen=True)
class ChartTitleConfig:
    title: str
    description: str
    alt_text: str


@dataclass(frozen=True)
class ChartsTitleConfig:
    charts: Mapping[str, ChartTitleConfig]


def normalize_description(desc: Union[str, list[str]]) -> str:
    """Normalize description to a single string."""
    if isinstance(desc, str):
        return desc
    if isinstance(desc, list):
        return "".join(map(str, desc))
    raise TypeError(f"description must be str or list of str, got {type(desc)}")


def load_title_config(path: str = "config/titles.json") -> dict:
    """Load title configuration from a JSON file."""
    config_file = Path(__file__).parent / path
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Title config file not found: {config_file}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON from {config_file}: {e}")


def deep_merge(default: dict, other: dict) -> dict:
    """Recursively merge two dictionaries."""
    merged = default.copy()
    for key, value in other.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def build_charts_config(user_title_config: str | None = None) -> ChartsTitleConfig:
    """Build ChartsTitleConfig from default and optional user config."""
    default_data = load_title_config()
    merged_data = default_data
    if user_title_config:
        user_data = load_title_config(user_title_config)
        merged_data = deep_merge(default=default_data, other=user_data)
    charts = {
        chart_id: ChartTitleConfig(
            title=chart_data.get("title", ""),
            description=normalize_description(chart_data.get("description", "")),
            alt_text=chart_data.get("alt_text", "")
        )
        for chart_id, chart_data in merged_data.items()
    }
    return ChartsTitleConfig(charts=charts)
