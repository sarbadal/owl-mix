from . import acf_pacf
from . import box_plot
from . import causality
from . import correlation
from . import ccf
from . import vif
from . import response_curve
from . import response_summary
from . import dist_numeric
from . import time_series

from .acf_pacf import AcfPacfConfigArgs, AcfPacf
from .box_plot import BoxPlotConfigArgs, BoxPlot
from .causality import CausalityConfigArgs, Causality
from .correlation import CorrelationConfigArgs, Correlation
from .ccf import CCFConfigArgs, CCF
from .vif import VifConfigArgs, Vif
from .response_curve import ResponseCurveConfigArgs, ResponseCurve
from .response_summary import SummaryConfigArgs, ResponseSummary
from .dist_numeric import DistNumericConfigArgs, DistNumeric
from .time_series import TimeSeriesPlotConfigArgs, TimeSeriesPlot


class Args:
    acf_pacf = acf_pacf
    box_plot = box_plot
    causality = causality
    correlation = correlation
    ccf = ccf
    vif = vif
    response_curve = response_curve
    response_summary = response_summary
    dist_numeric = dist_numeric
    time_series = time_series

__all__ = [
    "Args",
    "AcfPacfConfigArgs",
    "AcfPacf",
    "BoxPlotConfigArgs",
    "BoxPlot",
    "CausalityConfigArgs",
    "Causality",
    "CorrelationConfigArgs",
    "Correlation",
    "CCFConfigArgs",
    "CCF",
    "VifConfigArgs",
    "Vif",
    "ResponseCurveConfigArgs",
    "ResponseCurve",
    "SummaryConfigArgs",
    "ResponseSummary",
    "DistNumericConfigArgs",
    "DistNumeric",
    "TimeSeriesPlotConfigArgs",
    "TimeSeriesPlot"
]