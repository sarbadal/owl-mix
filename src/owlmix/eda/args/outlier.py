from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetOutlierConfigArgs(TypedDict):
    columns: NotRequired[list[str]]
    max_cols_per_chart: NotRequired[int]
    single_image: NotRequired[bool]


@dataclass
class Outlier:
    columns: list[str] | None = None
    max_cols_per_chart: int | None = None
    single_image: bool | None = None


def build(**values: Unpack[SetOutlierConfigArgs]) -> Outlier:
    """
    Build an Outlier configuration object from the provided values.
    Args:
        columns: Optional list of column names to include in the outlier analysis.
        max_cols_per_chart: Optional integer for max columns per chart.
        single_image: Optional boolean for single image output.
    Returns:
        Outlier object with the provided configuration.
    """
    values = values or {}
    return Outlier(
        columns=values.get("columns", None),
        max_cols_per_chart=values.get("max_cols_per_chart", 4), # default to 4 if not provided
        single_image=values.get("single_image", True) # default to True if not provided
    )
