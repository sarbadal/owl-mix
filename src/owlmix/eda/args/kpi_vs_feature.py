from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack
from ...typing.enums import Period
from ...typing.types import PeriodType


class SetKPIVsFeatureConfigArgs(TypedDict):
    target_column: NotRequired[str]
    columns: NotRequired[list[str]]
    period: NotRequired[PeriodType]
    date_column: NotRequired[str]
    agg_func: NotRequired[str]


@dataclass
class KPIVsFeature:
    target_column: str | None = None
    columns: list[str] | None = None
    period: PeriodType | None = Period.MONTHLY
    date_column: str | None = None
    agg_func: str | None = "sum"


def build(**values: Unpack[SetKPIVsFeatureConfigArgs]) -> KPIVsFeature:
    """
    Build a KPIVsFeature object from the provided keyword arguments.
    Args:
        target_column: str - name of the target column for KPI vs Feature analysis
        columns: list[str] - list of feature column names to compare against the target KPI
        period: PeriodType - time period for aggregating the data (e.g., daily, weekly, monthly)
        date_column: str - name of the date column for time-based analysis
        agg_func: str - aggregation function to apply to the data (e.g., sum, mean)
    Returns:        
        KPIVsFeature object with the provided configuration
    """
    values = values or {}
    return KPIVsFeature(
        target_column=values.get("target_column", None),
        columns=values.get("columns", None),
        period=values.get("period", Period.MONTHLY),  # default period to MONTHLY if not provided
        date_column=values.get("date_column", None),
        agg_func=values.get("agg_func", "sum")  # default agg_func to "sum" if not provided
    )