from . import acf_pacf
from . import box_plot
from . import causality
from . import correlation
from . import ccf
from . import vif
from . import response_curve

from .acf_pacf import AcfPacfConfigArgs, AcfPacf
from .box_plot import BoxPlotConfigArgs, BoxPlot
from .causality import CausalityConfigArgs, Causality
from .correlation import CorrelationConfigArgs, Correlation
from .ccf import CCFConfigArgs, CCF
from .vif import VifConfigArgs, Vif
from .response_curve import ResponseCurveConfigArgs, ResponseCurve


class Args:
    acf_pacf = acf_pacf
    box_plot = box_plot
    causality = causality
    correlation = correlation
    ccf = ccf
    vif = vif
    response_curve = response_curve


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
]