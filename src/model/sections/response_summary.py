from pydantic import BaseModel, RootModel, field_validator
from typing import Dict, List

class ContributionItem(BaseModel):
    """Schema for contribution item in response summary."""
    contribution: List[float]
    total_contribution: float
    average_contribution: float

    class Config:
        extra = 'forbid'

class CurveItem(BaseModel):
    """Schema for curve item in response summary."""
    feature: str
    input_value: List[float]
    observed_input_min: float
    observed_input_max: float
    predicted_target: List[float]
    contribution: ContributionItem
    predicted_target_raw: List[float]
    predicted_target_clipped: List[float]

    class Config:
        extra = 'forbid'

class ClassificationItem(BaseModel):
    """Schema for classification item in response summary."""
    zones: List[str]
    marginal: List[float]
    thresholds: Dict[str, float]

    class Config:
        extra = 'forbid'

class MetricItem(BaseModel):
    """Schema for metric item in response summary."""
    current_spend: float
    average_spend: float
    roi: float
    current_marginal_roi: float
    peak_marginal_roi: float
    saturation_point: float
    efficiency_ratio: float
    status: str

    class Config:
        extra = 'forbid'

class DataItem(BaseModel):
    """Schema for individual data items in response summary."""
    curve: CurveItem
    classification: ClassificationItem
    metrics: MetricItem

    class Config:
        extra = 'forbid'

class ResponseSummaryData(RootModel[Dict[str, DataItem]]):
    """Schema for response summary data."""
    @field_validator('root')
    @classmethod
    def validate_data(cls, value):
        statuses = ["underspend", "optimal", "saturated"]
        for key, item in value.items():
            if item.metrics.status not in statuses:
                raise ValueError(
                    f"Invalid status '{item.metrics.status}' for key '{key}'. "
                    f"Must be one of {statuses}."
                )
        return value

class ImageItem(RootModel[Dict[str, Dict[str, str]]]):
    """Schema for image item in response summary."""
    @field_validator('root')
    @classmethod
    def validate_images(cls, value):
        for key, images in value.items():
            if not isinstance(images, dict):
                raise ValueError(f"Images for key '{key}' must be a dictionary.")
            for img_key, img_value in images.items():
                if not isinstance(img_value, str):
                    raise ValueError(
                        f"Image value for '{img_key}' in key '{key}' must be a string."
                    )
        return value

class ChartItem(BaseModel):
    """Schema for chart information in response summary."""
    title: str
    description: str
    alt_text: str
    images: ImageItem

    class Config:
        extra = 'forbid'

class ResponseSummarySection(BaseModel):
    """Schema for response summary section."""
    chart: ChartItem
    data: ResponseSummaryData

    class Config:
        extra = 'forbid'