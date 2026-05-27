from pydantic import BaseModel, field_validator, Field
from typing import Dict, List

class CausalityTestResultItem(BaseModel):
    """Schema for causality test results."""
    variable: str
    best_lag: int
    p_value: float
    min_p_value: float
    score: float
    mape_score: float
    number_of_lags_tested: int
    causal: bool
    coefficient_sign: str

    class Config:
        extra = 'forbid'

class CausalityData(BaseModel):
    """Schema for causality test data."""
    causality_test_results: List[CausalityTestResultItem]
    error_threshold: float

    class Config:
        extra = 'forbid'

class CausalityChart(BaseModel):
    """Schema for causality test chart."""
    chart: Dict = Field(default_factory=dict)
    
    @field_validator('chart')
    @classmethod
    def validate_empty_dict(cls, value):
        if value != {}:
            raise ValueError("Chart data should be an empty dictionary.")
        return value

class CausalitySection(BaseModel):
    """Schema for causality test section."""
    data: CausalityData
    chart: CausalityChart

    class Config:
        extra = 'forbid'