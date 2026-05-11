from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class AcfPacfConfigArgs(TypedDict):
    """Configuration parameters for ACF/PACF analysis."""
    columns: NotRequired[list[str]]
    n_lags: NotRequired[int]
    acf_marker: NotRequired[str]
    pacf_marker: NotRequired[str]
    acf_stem: NotRequired[str]
    pacf_stem: NotRequired[str]
    acf_conf: NotRequired[str]
    pacf_conf: NotRequired[str]
    precision: NotRequired[int]


@dataclass
class AcfPacf:
    """Configuration parameters for ACF/PACF analysis."""
    columns: list[str] | None = None
    n_lags: int | None = 10
    acf_marker: str | None = "red"
    pacf_marker: str | None = "steelblue"
    acf_stem: str | None = "red"
    pacf_stem: str | None = "steelblue"
    acf_conf: str | None = "blue"
    pacf_conf: str | None = "gray"
    precision: int = 4


def build(**values: Unpack[AcfPacfConfigArgs]) -> AcfPacf:
    """
    Build an AcfPacf configuration object from the provided values.
    Args:
        columns: list of column names to include in the ACF/PACF analysis
        n_lags: number of lags to compute for ACF/PACF
    Returns:
        AcfPacf object with the provided configuration
    """
    values = values or {}
    return AcfPacf(**values)