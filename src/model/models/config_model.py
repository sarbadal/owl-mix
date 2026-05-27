from .base import BaseModelConfig
from .sections_model import SectionsModel

class ConfigModel(BaseModelConfig):
    """Model configuration for the entire model."""
    sections: SectionsModel

    def get_section(self, section_name: str):
        """Dynamically retrieve a section by name."""
        return getattr(self.sections, section_name, None)

    def has_section(self, section_name: str) -> bool:
        """Check if a section exists in the configuration."""
        return hasattr(self.sections, section_name)

    def available_sections(self):
        """Return a list of available sections in the configuration."""
        return [
            name 
            for name, value in self.sections.model_dump().items()
            if value is not None
        ]