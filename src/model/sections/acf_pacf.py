from pydantic import BaseModel
from typing import Dict, List

class AcfPacfData(BaseModel):
    """Schema for ACF and PACF sections."""
    column: str
    n_obs: int
    lags: List[int]
    acf: List[float]
    pacf: List[float]

    class Config:
        extra = 'forbid'

class AcfPacfChart(BaseModel):
    """Schema for ACF and PACF charts."""
    title: str
    description: str
    alt_text: str
    image: str  # Base64 encoded image (combined ACF and PACF chart)
    images: Dict[str, str]

    class Config:
        extra = 'forbid'

class AcfPacfSection(BaseModel):
    """Schema for ACF and PACF section."""
    data: List[AcfPacfData]
    chart: AcfPacfChart

    class Config:
        extra = 'forbid'