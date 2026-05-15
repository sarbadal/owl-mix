from . import acf_pacf
from . import box_plot
from . import causality
from . import correlation
from . import vif

from .acf_pacf import AcfPacfConfigArgs, AcfPacf
from .box_plot import BoxPlotConfigArgs, BoxPlot
from .causality import CausalityConfigArgs, Causality
from .correlation import CorrelationConfigArgs, Correlation
from .vif import VifConfigArgs, Vif


class Args:
    acf_pacf = acf_pacf
    box_plot = box_plot
    causality = causality
    correlation = correlation
    vif = vif


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
    "VifConfigArgs",
    "Vif",
]