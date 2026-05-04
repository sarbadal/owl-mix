from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetAcfPacfConfigArgs(TypedDict):
    columns: NotRequired[list[str]]
    n_lags: NotRequired[int]
    acf_marker: NotRequired[str]
    pacf_marker: NotRequired[str]
    acf_stem: NotRequired[str]
    pacf_stem: NotRequired[str]
    acf_conf: NotRequired[str]
    pacf_conf: NotRequired[str]


@dataclass
class AcfPacf:
    columns: list[str] | None = None
    n_lags: int | None = 10
    acf_marker: str | None = "red"
    pacf_marker: str | None = "steelblue"
    acf_stem: str | None = "red"
    pacf_stem: str | None = "steelblue"
    acf_conf: str | None = "blue"
    pacf_conf: str | None = "gray"


def build(**values: Unpack[SetAcfPacfConfigArgs]) -> AcfPacf:
    """
    Build an AcfPacf configuration object from the provided values.
    Args:
        columns: list of column names to include in the ACF/PACF analysis
        n_lags: number of lags to compute for ACF/PACF
    Returns:
        AcfPacf object with the provided configuration
    """
    values = values or {}
    return AcfPacf(
        columns=values.get("columns", None),
        n_lags=values.get("n_lags", 10)  # default n_lags to 10 if not provided
    )