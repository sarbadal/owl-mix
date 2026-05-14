import pandas as pd
from dataclasses import replace
from typing import Self, Unpack, Any

from ..typing.types import PeriodType, ComparisonType, PlotModeType
from ..params import Args
from ..params import AcfPacfConfigArgs
from ..params import CorrelationConfigArgs
from ..params import VifConfigArgs

OUTPUT_DIR = "output"


class ConfigBuilder:
    """
    Class to build and manage configuration settings for the report generation process, 
    including settings for various analysis sections such as ACF/PACF, CORRELATION, etc.
    """
    def __init__(self, df: pd.DataFrame, target_col: str, date_col: str, output_dir: str = OUTPUT_DIR):
        self.df = df.copy()
        self.target_col = target_col
        self.date_col = date_col
        self.output_dir = output_dir
        self._init_config()

    def _init_config(self) -> None:
        self.acf_pacf_config = Args.acf_pacf.build(columns=[self.target_col])
        self.vif_config = Args.vif.build(target_column=self.target_col)
        self.correlation_config = Args.correlation.build()

    def _validate_positive_int(self, value: Any, field_name: str) -> None:
        """Validate that a value is a positive integer."""
        if value is not None and (not isinstance(value, int) or value < 1):
            raise ValueError(f"{field_name} must be a positive integer")

    def update_config(self, **kwargs) -> Self:
        """
        Update configuration settings for various sections based on provided keyword arguments.
        Args:
            ``**kwargs``: Keyword arguments representing the configuration settings to be updated.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        config_mapping = {
            "acf_pacf_config": self.update_acf_pacf_config,
            "vif_config": self.update_vif_config,
            "correlation_config": self.update_correlation_config,
            # Add other config update methods here as needed
        }

        for key, value in kwargs.items():
            if key in config_mapping:
                config_mapping[key](**value)
        return self

    def update_acf_pacf_config(self, **kwargs: Unpack[AcfPacfConfigArgs]) -> Self:
        """
        Update the ACF/PACF configuration settings based on provided keyword arguments.
        Args:
            ``**kwargs``: Keyword arguments representing the ACF/PACF configuration settings to be updated.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        self.acf_pacf_config = replace(self.acf_pacf_config, **kwargs)
        return self

    def update_correlation_config(self, **kwargs: Unpack[CorrelationConfigArgs]) -> Self:
        """
        Update the Correlation configuration settings based on provided keyword arguments.
        Args:
            ``**kwargs``: Keyword arguments representing the Correlation configuration settings to be updated.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        self.correlation_config = replace(self.correlation_config, **kwargs)
        return self

    def update_vif_config(self, **kwargs: Unpack[VifConfigArgs]) -> Self:
        """
        Update the VIF configuration settings based on provided keyword arguments.
        Args:
            ``**kwargs``: Keyword arguments representing the VIF configuration settings to be updated.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        self.vif_config = replace(self.vif_config, **kwargs)
        return self