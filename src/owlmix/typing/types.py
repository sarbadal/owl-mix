# owlmix/typing/types.py
import pandas as pd
from typing import Callable, Dict, Protocol, Any, Self, Literal, Union, TypeAlias
from pathlib import Path
from .enums import Period, ComparisonType as ComparisonTypeEnum, PlotMode, ChartID

PeriodType: TypeAlias = Period | str
ComparisonType: TypeAlias = ComparisonTypeEnum | str
PlotModeType: TypeAlias = PlotMode | str
ChartIDType: TypeAlias = ChartID | str
