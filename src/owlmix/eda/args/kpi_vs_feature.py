from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack
from ...typing.enums import Period


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
    period: PeriodType | None = None
    date_column: str | None = None
    agg_func: str | None = None


def build(**values: Unpack[SetKPIVsFeatureConfigArgs]) -> KPIVsFeature:
    values = values or {}
    return KPIVsFeature(
        target_column=values.get("target_column", None),
        columns=values.get("columns", None),
        period=values.get("period", Period.MONTHLY),  # default period to MONTHLY if not provided
        date_column=values.get("date_column", None),
        agg_func=values.get("agg_func", "sum")  # default agg_func to "sum" if not provided
    )