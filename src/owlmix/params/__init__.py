from . import acf_pacf
from . import causality
from . import correlation
from . import vif

from .acf_pacf import AcfPacfConfigArgs, AcfPacf
from .causality import CausalityConfigArgs, Causality
from .correlation import CorrelationConfigArgs, Correlation
from .vif import VifConfigArgs, Vif


class Args:
    acf_pacf = acf_pacf
    causality = causality
    correlation = correlation
    vif = vif


__all__ = [
    "Args",
    "AcfPacfConfigArgs",
    "AcfPacf",
    "CausalityConfigArgs",
    "Causality",
    "CorrelationConfigArgs",
    "Correlation",
    "VifConfigArgs",
    "Vif"
]