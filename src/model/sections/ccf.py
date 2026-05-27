from pydantic import BaseModel, RootModel, Field, field_validator
from typing import Any, Dict, List

class ResultItem(BaseModel):
    """Schema for individual CCF result items."""
    target_column: str
    feature: str
    version: str
    lag: int
    correlation: float

    class Config:
        extra = 'forbid'

class CCFResults(RootModel[Dict[str, List[ResultItem]]]):
    """Schema for CCF item."""
    @field_validator('root')
    @classmethod
    def validate_ccf_results(cls, value):
        if not isinstance(value, dict):
            raise ValueError("CCF results must be a dictionary.")
        for key, val in value.items():
            if not isinstance(key, str):
                raise ValueError("Keys in CCF results must be strings.")
            if not isinstance(val, list) or not all(isinstance(item, ResultItem) for item in val):
                raise ValueError("Values in CCF results must be lists of ResultItem.")
        return value

class CCFSummaryTable(BaseModel):
    """Schema for CCF summary table."""
    target_column: str
    feature: str
    version: str
    max_correlation: float
    lag_at_max: int
    correlation_at_lag_0: float

    class Config:
        extra = 'forbid'

class KPIFeature(BaseModel):
    """Schema for KPI data."""
    raw: List[float]
    smooth: List[float]
    normalized: List[float]
    min: float
    max: float
    points: str

    class Config:
        extra = 'forbid'

class LinesItem(BaseModel):
    """Schema for lines item."""
    time: List[str]
    kpi: KPIFeature
    feature: KPIFeature

    class Config:
        extra = 'forbid'

class CCF(BaseModel):
    """Schema for CCF section."""
    ccf_results: CCFResults
    summary_table: List[CCFSummaryTable]

    class Config:
        extra = 'forbid'

class CCFData(BaseModel):
    """Schema for CCF data."""
    ccf: CCF
    lines: Dict[str, LinesItem]
    
    class Config:
        extra = 'forbid'

class CCFSection(BaseModel):
    """Schema for CCF section."""
    data: CCFData
    chart: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = 'forbid'