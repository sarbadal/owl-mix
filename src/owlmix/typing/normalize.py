# owlmix/typing/normalize.py
from typing import Any

from .constrants import PERIOD_VALUES, COMPARISON_TYPE_VALUES, MODE_VALUES, CHART_IDS
from .enums import Period, ComparisonType, PlotMode, ChartID


def _to_str_value(value: Any) -> str:
    if isinstance(value, tuple):
        return str(value[0])
    return str(value)


def normalize_period(period: Period | str) -> str:
    if isinstance(period, Period):
        period = _to_str_value(period.value)

    if period not in PERIOD_VALUES:
        raise ValueError(f"Invalid period '{period}'. Must be one of {PERIOD_VALUES}")

    return period


def normalize_comparison_type(comparison_type: ComparisonType | str) -> str:
    if isinstance(comparison_type, ComparisonType):
        comparison_type = _to_str_value(comparison_type.value)

    if comparison_type not in COMPARISON_TYPE_VALUES:
        raise ValueError(
            f"Invalid comparison_type '{comparison_type}'. "
            f"Must be one of {COMPARISON_TYPE_VALUES}"
        )

    return comparison_type


def normalize_plot_mode(plot_mode: PlotMode | str) -> str:
    if isinstance(plot_mode, PlotMode):
        plot_mode = _to_str_value(plot_mode.value)

    if plot_mode not in MODE_VALUES:
        raise ValueError(
            f"Invalid plot_mode '{plot_mode}'. "
            f"Must be one of {MODE_VALUES}"
        )

    return plot_mode


def normalize_chart_id(id: ChartID | str) -> str:
    if isinstance(id, ChartID):
        id = _to_str_value(id.value)

    if id not in CHART_IDS:
        raise ValueError(
            f"Invalid chart id '{id}'. "
            f"Must be one of {CHART_IDS}"
        )

    return id
