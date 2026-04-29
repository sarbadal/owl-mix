from . import acf_pacf
from . import categorical_columns
from . import causality_test
from . import corr_chart_layout
from . import correlation
from . import kpi_vs_feature
from . import outlier
from . import time_aggregator
from . import time_comparison
from . import time_comparison_chart
from . import time_series
from . import vif


from .acf_pacf import SetAcfPacfConfigArgs
from .categorical_columns import SetCategoricalColumnsConfigArgs
from .causality_test import SetCausalityTestConfigArgs
from .corr_chart_layout import SetCorrChartLayoutConfigArgs
from .correlation import SetCorrelationConfigArgs
from .kpi_vs_feature import SetKPIVsFeatureConfigArgs
from .outlier import SetOutlierConfigArgs
from .time_aggregator import SetTimeAggregatorConfigArgs
from .time_comparison_chart import SetTimeComparisonChartConfigArgs
from .time_comparison import SetTimeComparisonConfigArgs
from .time_series import SetTimeSeriesConfigArgs
from .vif import SetVIFConfigArgs


class Args:
    acf_pacf = acf_pacf
    categorical_columns = categorical_columns
    causality_test = causality_test
    corr_chart_layout = corr_chart_layout
    correlation = correlation
    kpi_vs_feature = kpi_vs_feature
    outlier = outlier
    time_aggregator = time_aggregator
    time_comparison = time_comparison
    time_comparison_chart = time_comparison_chart
    time_series = time_series
    vif = vif


__all__ = [
    "Args",
    "SetAcfPacfConfigArgs",
    "SetCategoricalColumnsConfigArgs",
    "SetCausalityTestConfigArgs",
    "SetCorrChartLayoutConfigArgs",
    "SetCorrelationConfigArgs",
    "SetKPIVsFeatureConfigArgs",
    "SetOutlierConfigArgs",
    "SetTimeAggregatorConfigArgs",
    "SetTimeComparisonChartConfigArgs",
    "SetTimeComparisonConfigArgs",
    "SetTimeSeriesConfigArgs",
    "SetVIFConfigArgs"
]