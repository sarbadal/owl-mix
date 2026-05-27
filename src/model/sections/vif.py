from pydantic import BaseModel
from typing import Dict, List

class VIFData(BaseModel):
    """Schema for VIF data."""
    feature: List[str]
    vif: List[float]
    color: List[str]

    class Config:
        extra = 'forbid'

class VIFChart(BaseModel):
    """Schema for VIF chart."""
    title: str
    description: str
    alt_text: str
    image: str

    class Config:
        extra = 'forbid'

class VIFSection(BaseModel):
    """Schema for VIF section."""
    data: VIFData
    chart: VIFChart

    class Config:
        extra = 'forbid'