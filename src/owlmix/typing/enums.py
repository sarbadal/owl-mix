# owlmix/typing/enums.py
import json
from enum import Enum


class BaseEnum(Enum):
    def __init__(self, value, label=None):
        self._value_ = value
        self.label = label or value

    @classmethod
    def list(cls):
        return list(cls)

    @classmethod
    def names(cls):
        return [item.name for item in cls]

    @classmethod
    def values(cls):
        return [item.value for item in cls]

    @classmethod
    def options(cls):
        return [
            {"id": item.value, "name": item.name, "value": item.value, "label": item.label} 
            for item in cls
        ]

    @classmethod
    def pretty_options(cls):
        return json.dumps(cls.options(), indent=2)


class Period(BaseEnum):
    DAILY = ("daily", "Daily")
    WEEKLY = ("weekly", "Weekly")
    MONTHLY = ("monthly", "Monthly")
    YEARLY = ("yearly", "Yearly")


class ComparisonType(BaseEnum):
    YoY = ("yoy", "Year over Year")
    QoQ = ("qoq", "Quarter over Quarter")
    MoM = ("mom", "Month over Month")
    WoW = ("wow", "Week over Week")
    YoY_MONTH = ("yoy_month", "This Year vs Last Year Same Month")
    YoY_QUARTER = ("yoy_quarter", "This Year vs Last Year Same Quarter")
    YoY_WEEK = ("yoy_week", "This Year vs Last Year Same Week")


class PlotMode(BaseEnum):
    ABSOLUTE = ("absolute", "Absolute Values")
    PCT_CHANGE = ("pct_change", "Percentage Change")
    DUAL = ("dual", "Dual")


class ChartID(BaseEnum):
    VIF_CHART = ("vif_chart", "VIF Chart")
    ACF_PACF_CHART = ("acf_pacf_chart", "ACF PACF Chart")
    KPI_VS_FEATURE_CHART = ("kpi_vs_feature_chart", "KPI vs Feature Chart")
    DISTRIBUTION_CHART = ("distribution_chart", "Distribution Chart")
    CATEGORICAL_DISTRIBUTION_CHART = ("categorical_distribution_chart", "Categorical Distribution Chart")
    CORRELATION_CHART = ("correlation_chart", "Correlation Chart")
    LAG_CORRELATION_CHART = ("lag_correlation_chart", "Lag Correlation Chart")
    TIME_SERIES_CHART = ("time_series_chart", "Time Series Chart")
    OUTLIERS_CHART = ("outliers_chart", "Outliers Chart")
    COMPARISON_CHART = ("comparison_chart", "Comparison Chart")


class SectionEnum(BaseEnum):
    ACF_PACF = ("acf_pacf", "ACF and PACF Analysis")
    BOX_PLOT = ("box_plot", "Box Plot Analysis")
    CAUSALITY = ("causality", "Causality Analysis")
    CCF = ("ccf", "Cross-Correlation Function Analysis")
    CORRELATION = ("correlation", "Correlation Analysis")
    RESPONSE_SUMMARY = ("response_summary", "Response Summary Analysis")
    VIF = ("vif", "Variance Inflation Factor Analysis")
    DIST_NUMERIC = ("dist_numeric", "Distribution of Numerical Columns Analysis")
