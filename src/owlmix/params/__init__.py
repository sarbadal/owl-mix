from . import acf_pacf
from . import correlation
from . import vif

from .acf_pacf import AcfPacfConfigArgs, AcfPacf
from .correlation import CorrelationConfigArgs, Correlation
from .vif import VifConfigArgs, Vif


class Args:
    acf_pacf = acf_pacf
    correlation = correlation
    vif = vif


__all__ = [
    "Args",
    "AcfPacfConfigArgs",
    "AcfPacf",
    "CorrelationConfigArgs",
    "Correlation",
    "VifConfigArgs",
    "Vif"
]