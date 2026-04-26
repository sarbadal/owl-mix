# owlmix/typing/normalize.py
from .constrants import PERIOD_VALUES, COMPARISON_TYPE_VALUES
from .enums import Period, ComparisonType

VALID_PERIODS = set(PERIOD_VALUES)


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