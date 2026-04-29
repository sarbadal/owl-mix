from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetCorrelationConfigArgs(TypedDict):
    columns: NotRequired[list[str]]


@dataclass
class Correlation:
    columns: list[str] | None = None


def build(**values: Unpack[SetCorrelationConfigArgs]) -> Correlation:
    """
    Build a Correlation object from the provided keyword arguments.
    Args:
        columns: Optional list of column names to include in the correlation analysis.
    Returns:
        Correlation object with the provided configuration.
    """
    values = values or {}
    return Correlation(
        columns=values.get("columns", None)
    )