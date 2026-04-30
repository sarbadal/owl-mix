from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetAcfPacfConfigArgs(TypedDict):
    columns: NotRequired[list[str]]
    n_lags: NotRequired[int]


@dataclass
class AcfPacf:
    columns: list[str] | None = None
    n_lags: int | None = 10


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