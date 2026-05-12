# owlmix/typing/types.py
import pandas as pd
from typing import Callable, Dict, Protocol, Any, Self, Literal, Union
from pathlib import Path
from .enums import Period, ComparisonType, PlotMode, ChartID


PeriodType = Union[Period, str]
ComparisonType = Union[ComparisonType, str]
PlotModeType = Union[PlotMode, str]
ChartIDType = Union[ChartID, str]
