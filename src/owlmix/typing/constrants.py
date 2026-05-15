"""
This module defines constant values used across the owlmix library,
such as default thresholds, default lag values, and other fixed parameters that
are commonly referenced in analysis and plotting functions.
"""

#: is used to denote inline comments that explain the purpose of each constant. 
# This is mainly for Sphinx documentation generation, allowing these comments to be 
# included in the generated docs. The constants defined here are intended to be imported 
# and used throughout the owlmix library

#: Time periods for time series analysis and comparison
PERIOD_VALUES = ("daily", "weekly", "monthly", "yearly")

#: Types of comparisons for time series analysis
COMPARISON_TYPE_VALUES = ("yoy", "qoq", "mom", "wow", "yoy_month", "yoy_quarter", "yoy_week")

#: Modes for data representation
MODE_VALUES = ("absolute", "pct_change", "dual")

#: Identifiers for different types of charts
CHART_IDS = (
    "vif_chart",
    "acf_pacf_chart",
    "kpi_vs_feature_chart",
    "distribution_chart",
    "categorical_distribution_chart",
    "correlation_chart",
    "lag_correlation_chart",
    "time_series_chart",
    "outliers_chart",
    "comparison_chart"

)