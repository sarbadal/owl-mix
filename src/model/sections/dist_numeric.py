from pydantic import BaseModel, RootModel, field_validator
from typing import Dict, List

class Images(RootModel[Dict[str, str]]):
    """Schema for images in distribution numeric."""
    @field_validator('root')
    @classmethod
    def validate_images(cls, value):
        for key, img_value in value.items():
            if not isinstance(img_value, str):
                raise ValueError(f"Image value for '{key}' must be a string.")
        return value

class Chart(BaseModel):
    """Schema for distribution numeric chart."""
    title: str
    description: str
    alt_text: str
    images: Images

    class Config:
        extra = 'forbid'

class DistributionNumericSection(BaseModel):
    """Schema for distribution numeric section."""
    data: Dict[str, List[float]] = {}
    chart: Chart

    class Config:
        extra = 'forbid'