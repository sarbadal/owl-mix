from pydantic import BaseModel
from typing import Dict, List

class TimeSeriesDecompositionImages(BaseModel):
    """Schema for time series decomposition data."""
    observed: str
    trend: str
    seasonal: str
    residuals: str
    
    class Config:
        extra = 'forbid'

class TimeSeriesDecompositionChart(BaseModel):
    """Schema for time series decomposition chart."""
    title: str
    description: str
    alt_text: str
    images: TimeSeriesDecompositionImages

    class Config:
        extra = 'forbid'


class TimeSeriesDecompositionSection(BaseModel):
    """Schema for time series decomposition section."""
    data: Dict[str, List[float]] = {}
    chart: TimeSeriesDecompositionChart

    class Config:
        extra = 'forbid'