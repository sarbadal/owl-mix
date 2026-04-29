from dataclasses import dataclass
from typing import TypedDict, NotRequired, Unpack


class SetCategoricalColumnsConfigArgs(TypedDict):
    columns: NotRequired[list[str]]


@dataclass
class CategoricalColumns:
    columns: list[str] | None = None


def build(**values: Unpack[SetCategoricalColumnsConfigArgs]) -> CategoricalColumns:
    """
    Build a CategoricalColumns configuration object from the provided values.
    Args:
        columns: list of column names to include in the categorical distribution analysis
    Returns:
        CategoricalColumns object with the provided configuration
    """
    values = values or {}
    return CategoricalColumns(
        columns=values.get("columns", None)
    )

