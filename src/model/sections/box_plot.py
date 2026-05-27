from pydantic import BaseModel
from typing import Dict, List

class OriginalItem(BaseModel):
    """Schema for individual data items in box plot."""
    column: str
    min: float
    Q1: float
    median: float
    mean: float
    Q3: float
    max: float
    outliers_count: int
    outliers: List[float]

    class Config:
        extra = 'forbid'

class Ticks(BaseModel):
    """Schema for ticks in box plot."""
    value: float
    label: str
    x: float

    class Config:
        extra = 'forbid'

class ScalerDataItem(BaseModel):
    """Schema for individual data items in box plot after scaling."""
    x: str
    x_min: float
    x_q1: float
    x_median: float
    x_mean: float
    x_q3: float
    x_max: float
    x_outliers: List[float]
    domain_min: float
    domain_max: float
    ticks: List[Ticks]

    class Config:
        extra = 'forbid'

class BoxPlotData(BaseModel):
    """Schema for box plot data."""
    original: List[OriginalItem]
    scaler_data: List[ScalerDataItem]

    class Config:
        extra = 'forbid'

class BoxPlotChart(BaseModel):
    """Schema for box plot chart."""
    title: str
    description: str
    alt_text: str
    images: Dict[str, str]

    class Config:
        extra = 'forbid'

class BoxPlotSection(BaseModel):
    """Schema for box plot section."""
    data: BoxPlotData
    chart: BoxPlotChart

    class Config:
        extra = 'forbid'