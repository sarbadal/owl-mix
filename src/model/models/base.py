from pydantic import BaseModel, ConfigDict

class BaseModelConfig(BaseModel):
    """Base model configuration for all models."""
    model_config = ConfigDict(
        extra='forbid',
        validate_assignment=True,
    )