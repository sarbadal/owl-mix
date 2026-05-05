# owlmix/typing/normalize.py
from .constrants import PERIOD_VALUES, COMPARISON_TYPE_VALUES, MODE_VALUES, CHART_IDS
from .enums import Period, ComparisonType, PlotMode, ChartID


def normalize_period(period: Period | str) -> str:
    if isinstance(period, Period):
        period = period.value

    if period not in PERIOD_VALUES:
        raise ValueError(f"Invalid period '{period}'. Must be one of {PERIOD_VALUES}")

    return period


def normalize_comparison_type(comparison_type: ComparisonType | str) -> str:
    if isinstance(comparison_type, ComparisonType):
        comparison_type = comparison_type.value

    if comparison_type not in COMPARISON_TYPE_VALUES:
        raise ValueError(
            f"Invalid comparison_type '{comparison_type}'. "
            f"Must be one of {COMPARISON_TYPE_VALUES}"
        )

    return comparison_type


def normalize_plot_mode(plot_mode: PlotMode) -> str:
    if isinstance(plot_mode, PlotMode):
        plot_mode = plot_mode.value

    if plot_mode not in MODE_VALUES:
        raise ValueError(
            f"Invalid plot_mode '{plot_mode}'. "
            f"Must be one of {MODE_VALUES}"
        )

    return plot_mode


def normalize_chart_id(id: ChartID) -> str:
    if isinstance(id, ChartID):
        id = id.value

    if id not in CHART_IDS:
        raise ValueError(
            f"Invalid chart id '{id}'. "
            f"Must be one of {CHART_IDS}"
        )

    return id
