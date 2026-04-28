# owlmix/typing/types.py
from typing import Literal, Union
from .enums import Period, ComparisonType, PlotMode, ChartID


PeriodType = Union[Period, str]

ComparisonType = Union[ComparisonType, str]

PlotModeType = Union[PlotMode, str]

ChartIDType = Union[ChartID, str]