from pydantic import create_model, ConfigDict

from .registry import SECTION_SCHEMA_REGISTRY

SectionsModel = create_model(
    "SectionsModel",
    **{
        section_name: (section_model | None, None) 
        for section_name, section_model in SECTION_SCHEMA_REGISTRY.items()
    }
)

SectionsModel.model_config = ConfigDict(extra="forbid")