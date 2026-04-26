# owlmix/typing/types.py
from typing import Literal, Union
from .enums import Period, ComparisonType
from .constrants import PERIOD_VALUES, COMPARISON_TYPE_VALUES


# PeriodLiteral = Literal[PERIOD_VALUES]

PeriodType = Union[Period, str]

ComparisonType = Union[ComparisonType, str]