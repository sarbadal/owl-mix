from . import acf_pacf
from . import vif

from .acf_pacf import AcfPacfConfigArgs, AcfPacf
from .vif import VifConfigArgs, Vif


class Args:
    acf_pacf = acf_pacf
    vif = vif


__all__ = [
    "Args",
    "AcfPacfConfigArgs",
    "AcfPacf",
    "VifConfigArgs",
    "Vif"
]