from pydantic import BaseModel, RootModel, field_validator
from typing import Dict, List

from .constand import corr_features

class LagCorrItem(RootModel[Dict[str, float]]):
    @field_validator('root')
    @classmethod
    def validate_keys(cls, value):
        keys = list(value.keys())
        try:
            int_keys = sorted([int(k) for k in keys])
        except ValueError:
            raise ValueError(
                "Lagged correlation matrix keys must be integers "
                "as strings (e.g., '0', '1', '2')."
            )

        if any(int(k) < 0 for k in keys):
            raise ValueError("Lagged correlation matrix keys must be non-negative integers as strings.")

        expected_keys = list(range(len(int_keys)))
        if int_keys != expected_keys:
            raise ValueError(
                f"Lagged correlation matrix keys must be consecutive integers starting from 0 as strings. "
                f"Expected keys: {expected_keys}, but got: {int_keys}."
            )
        return value

class CorrItem(BaseModel):
    """Schema for correlation matrix."""
    correlation_matrix: Dict[str, Dict[str, float]]
    lagged_correlation_matrix: Dict[str, LagCorrItem]

    @field_validator('correlation_matrix')
    @classmethod
    def validate_corr_matrix(cls, value):
        if set(value.keys()) != set(corr_features):
            raise ValueError(f"Correlation matrix keys must be {corr_features}.")

        if any(set(inner.keys()) != set(corr_features) for inner in value.values()):
            raise ValueError(
                f"Each inner dictionary in correlation matrix must have keys {corr_features}."
            )
        return value

class ImageDict(BaseModel):
    """Schema for image dictionary."""
    correlation_matrix: str  # Base64 encoded image
    lagged_correlation_matrix: str  # Base64 encoded image

    class Config:
        extra = 'forbid'

class CorrChartItem(BaseModel):
    """Schema for correlation matrix chart."""
    title: str
    description: str
    alt_text: str
    images: ImageDict

    class Config:
        extra = 'forbid'

class CorrelationSection(BaseModel):
    """Schema for correlation matrix section."""
    data: CorrItem
    chart: CorrChartItem

    class Config:
        extra = 'forbid'