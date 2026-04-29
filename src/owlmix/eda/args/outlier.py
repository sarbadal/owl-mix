from dataclasses import dataclass
from typing import TypedDict, NotRequired

class SetOutlierConfigArgs(TypedDict):
    columns: NotRequired[list[str]]
    max_cols_per_chart: NotRequired[int]
    single_image: NotRequired[bool]

@dataclass
class OutlierConfigArgs:
    columns: list[str] | None = None
    max_cols_per_chart: int | None = None
    single_image: bool | None = None

def build(data: OutlierConfigArgs) -> SetOutlierConfigArgs:
    return {
        "columns": data.columns,
        "max_cols_per_chart": data.max_cols_per_chart,
        "single_image": data.single_image
    }
