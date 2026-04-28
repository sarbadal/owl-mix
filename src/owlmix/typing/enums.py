# owlmix/typing/enums.py
from enum import Enum
from .constrants import PERIOD_VALUES


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


class PlotMode(str, Enum):
    ABSOLUTE = "absolute"
    PCT_CHANGE = "pct_change"
    DUAL = "dual"


class ChartID(str, Enum):
    VIF_CHART = "vif_chart"
    ACF_PACF_CHART = "acf_pacf_chart"
    KPI_VS_FEATURE_CHART = "kpi_vs_feature_chart"
    DISTRIBUTION_CHART = "distribution_chart"
    CATEGORICAL_DISTRIBUTION_CHART = "categorical_distribution_chart"
    CORRELATION_CHART = "correlation_chart"
    LAG_CORRELATION_CHART = "lag_correlation_chart"
    TIME_SERIES_CHART = "time_series_chart"
    OUTLIERS_CHART = "outliers_chart"
    COMPARISON_CHART = "comparison_chart"
