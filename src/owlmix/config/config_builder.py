import pandas as pd
import yaml
import json
from dataclasses import replace
from typing import Self, Unpack, Any

from ..typing.types import PeriodType, ComparisonType, PlotModeType
from ..params import Args
from ..params import AcfPacfConfigArgs
from ..params import BoxPlotConfigArgs
from ..params import CausalityConfigArgs
from ..params import CorrelationConfigArgs
from ..params import CCFConfigArgs
from ..params import VifConfigArgs
from ..params import ResponseCurveConfigArgs
from ..params import SummaryConfigArgs
from ..params import DistNumericConfigArgs
from ..params import TimeSeriesPlotConfigArgs

OUTPUT_DIR = "outputs"


class ConfigBuilder:
    """
    Class to build and manage configuration settings for the report generation process, 
    including settings for various analysis sections such as ACF/PACF, CORRELATION, etc.
    """
    def __init__(self, df: pd.DataFrame, target_col: str, date_col: str, output_dir: str = OUTPUT_DIR):
        self.df = df.copy(deep=True)
        self.target_col = target_col
        self.date_col = date_col
        self.output_dir = output_dir
        self._init_config()

    def _init_config(self) -> None:
        self.acf_pacf_config = Args.acf_pacf.build(columns=[self.target_col])
        self.box_plot_config = Args.box_plot.build()
        self.vif_config = Args.vif.build(target_column=self.target_col)
        self.causality_config = Args.causality.build(target_column=self.target_col)
        self.correlation_config = Args.correlation.build()
        self.ccf_config = Args.ccf.build(time_column=self.date_col, target_column=self.target_col)
        self.response_curve_config = Args.response_curve.build(target_column=self.target_col)
        self.response_summary_config = Args.response_summary.build(target_column=self.target_col)
        self.dist_numeric_config = Args.dist_numeric.build()
        self.time_series_config = Args.time_series.build(date_column=self.date_col, target_column=self.target_col)

    def _validate_positive_int(self, value: Any, field_name: str) -> None:
        """Validate that a value is a positive integer."""
        if value is not None and (not isinstance(value, int) or value < 1):
            raise ValueError(f"{field_name} must be a positive integer")

    def _config_mapping(self) -> dict:
        """Return a mapping of configuration section names to their corresponding update methods."""
        return {
            "acf_pacf": self.update_acf_pacf_config,
            "vif": self.update_vif_config,
            "correlation": self.update_correlation_config,
            "causality": self.update_causality_config,
            "box_plot": self.update_box_plot_config,
            "ccf": self.update_ccf_config,
            "response_curve": self.update_response_curve_config,
            "response_summary": self.update_response_summary_config,
            "dist_numeric": self.update_dist_numeric_config,
            "time_series": self.update_time_series_config,
        }

    def update_config_from_dict(self, config_dict: dict, strict: bool = True) -> Self:
        """
        Update configuration settings based on a dictionary.
        Args:
            config_dict (dict): A dictionary containing the configuration settings to be updated.
            strict (bool): Whether to raise an error if the dictionary contains invalid keys. Default is True.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        config_mapping = self._config_mapping()

        if not isinstance(config_dict, dict):
            raise ValueError("Configuration must be a dictionary")

        unknown_keys = [key for key in config_dict if key not in config_mapping]
        if unknown_keys and strict:
            allowed_keys = ", ".join(sorted(config_mapping.keys()))
            unknown_keys_msg = ", ".join(sorted(unknown_keys))
            raise ValueError(
                f"Unknown config section(s): {unknown_keys_msg}. Allowed sections: {allowed_keys}"
            )

        filtered_config = {
            key: value
            for key, value in config_dict.items()
            if key in config_mapping
        }

        for section_name, section_payload in filtered_config.items():
            if not isinstance(section_payload, dict):
                raise ValueError(
                    f"Section '{section_name}' must be a dictionary, got {type(section_payload).__name__}"
                )

        return self.update_config(**filtered_config)

    def update_config_from_yaml(self, path: str, strict: bool = True) -> Self:
        """
        Update configuration settings based on a YAML file.
        Args:
            path (str): The path to the YAML file containing the configuration settings.
            strict (bool): Whether to raise an error if the YAML file contains invalid keys. Default is True.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        with open(path, "r", encoding="utf-8") as file:
            yaml_config = yaml.safe_load(file) or {}
        if not isinstance(yaml_config, dict):
            raise ValueError("YAML configuration must be a dictionary at top level")

        return self.update_config_from_dict(yaml_config, strict=strict)

    def update_config_from_json(self, path: str, strict: bool = True) -> Self:
        """
        Update configuration settings based on a JSON file.
        Args:
            path (str): The path to the JSON file containing the configuration settings.
            strict (bool): Whether to raise an error if the JSON file contains invalid keys. Default is True.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        with open(path, "r", encoding="utf-8") as file:
            json_config = json.load(file)
        if not isinstance(json_config, dict):
            raise ValueError("JSON configuration must be a dictionary at top level")

        return self.update_config_from_dict(json_config, strict=strict)

    def update_config(self, **kwargs) -> Self:
        """
        Update configuration settings for various sections based on provided keyword arguments.
        Args:
            ``**kwargs``: Keyword arguments representing the configuration settings to be updated.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        config_mapping = self._config_mapping()

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

    def update_box_plot_config(self, **kwargs: Unpack[BoxPlotConfigArgs]) -> Self:
        """
        Update the Box Plot configuration settings based on provided keyword arguments.
        Args:
            ``**kwargs``: Keyword arguments representing the Box Plot configuration settings to be updated.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        self.box_plot_config = replace(self.box_plot_config, **kwargs)
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

    def update_causality_config(self, **kwargs: Unpack[CausalityConfigArgs]) -> Self:
        """
        Update the Causality configuration settings based on provided keyword arguments.
        Args:
            ``**kwargs``: Keyword arguments representing the Causality configuration settings to be updated.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        self.causality_config = replace(self.causality_config, **kwargs)
        return self

    def update_ccf_config(self, **kwargs: Unpack[CCFConfigArgs]) -> Self:
        """
        Update the CCF configuration settings based on provided keyword arguments.
        Args:
            ``**kwargs``: Keyword arguments representing the CCF configuration settings to be updated.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        self.ccf_config = replace(self.ccf_config, **kwargs)
        return self

    def update_response_curve_config(self, **kwargs: Unpack[ResponseCurveConfigArgs]) -> Self:
        """
        Update the Response Curve configuration settings based on provided keyword arguments.
        Args:
            ``**kwargs``: Keyword arguments representing the Response Curve configuration settings to be updated.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        self.response_curve_config = replace(self.response_curve_config, **kwargs)
        return self

    def update_response_summary_config(self, **kwargs: Unpack[SummaryConfigArgs]) -> Self:
        """
        Update the Response Summary configuration settings based on provided keyword arguments.
        Args:
            ``**kwargs``: Keyword arguments representing the Response Summary configuration settings to be updated.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        self.response_summary_config = replace(self.response_summary_config, **kwargs)
        return self

    def update_dist_numeric_config(self, **kwargs: Unpack[DistNumericConfigArgs]) -> Self:
        """
        Update the Distribution of Numerical Columns configuration settings based on provided keyword arguments.
        Args:
            ``**kwargs``: Keyword arguments representing the Distribution of Numerical Columns configuration settings to be updated.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        self.dist_numeric_config = replace(self.dist_numeric_config, **kwargs)
        return self

    def update_time_series_config(self, **kwargs: Unpack[TimeSeriesPlotConfigArgs]) -> Self:
        """
        Update the Time Series configuration settings based on provided keyword arguments.
        Args:
            ``**kwargs``: Keyword arguments representing the Time Series configuration settings to be updated.
        Returns:
            Self: The current instance of the ConfigBuilder.
        """
        self.time_series_config = replace(self.time_series_config, **kwargs)
        return self