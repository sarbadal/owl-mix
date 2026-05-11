from . import acf_pacf

from .acf_pacf import AcfPacfConfigArgs, AcfPacf


class Args:
    acf_pacf = acf_pacf


__all__ = [
    "Args",
    "AcfPacfConfigArgs",
    "AcfPacf",
]