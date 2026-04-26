# owlmix/typing/enums.py
from enum import Enum
from .constrants import PERIOD_VALUES


# Period = Enum(
#     "Period",
#     {value.upper(): value for value in PERIOD_VALUES},
#     type=str
# )

class Period(str, Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'


class ComparisonType(str, Enum):
    YoY = "yoy"
    QoQ = "qoq"
    MoM = "mom"
    WoW = "wow"
    YoY_MONTH = "yoy_month"
    YoY_QUARTER = "yoy_quarter"
    YoY_WEEK = "yoy_week"
