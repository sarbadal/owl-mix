import os
import json
from dataclasses import dataclass

from owlmix.eda.summary_builder_config import SummaryBuilderConfig


@dataclass
class ChartTitleConfig:
    title: str
    description: str
    alt_text: str


@dataclass
class ChartsTitleConfig:
    charts: dict[str, ChartTitleConfig]


def normalize_description(desc: str | list[str]) -> str:
    if isinstance(desc, str):
        return desc

    if isinstance(desc, list):
        return "".join(str(item) for item in desc)

    raise TypeError(
        f"description must be str or list of str, got {type(desc)}"
    )


def load_title_config(path: str = "config/titles.json") -> dict:
    """Load title configuration from a JSON file."""
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(curr_dir, path)

    with open(config_file, "r") as f:
        return json.load(f)


def deep_merge(default: dict, other: dict) -> dict:
    """Create a new dict with deep merge."""
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

    default_data: dict = load_title_config()

    if user_title_config:
        user_data: dict = load_title_config(user_title_config)
        merged_data: dict = deep_merge(
            default=default_data,
            other=user_data
        )

    else:
        merged_data = default_data

    charts = {}

    for chart_id, chart_data in merged_data.items():
        normalized_data = chart_data.copy()

        # Normalize description
        normalized_data["description"] = normalize_description(
            chart_data.get("description", "")
        )

        charts[chart_id] = ChartTitleConfig(**normalized_data)

    return ChartsTitleConfig(charts=charts)
