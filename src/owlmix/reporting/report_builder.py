"""
This module defines the SummaryBuilder class, which orchestrates the generation of
Exploratory Data Analysis (EDA) reports, including both textual and chart-based sections.
It provides a flexible API to add, include, exclude, and reorder report sections and charts,
and to output the report as a JSON file.
"""

import os
import base64
import pandas as pd
import json
from typing import Any, Self, Callable, Optional, Dict, List, Set, Union
from collections import OrderedDict
from dataclasses import dataclass, field

from . import sections
from ..typing.enums import SectionEnum
from ..registry.registry import ANALYZERS_REGISTRY, SECTION_BUILDERS
from ..config.config_builder import ConfigBuilder

DEFAULT_OUTJSON_FILENAME = "report.json"


@dataclass
class SectionContent:
    """
    Data class to represent the content of a report section.

    Attributes:
        data (Dict[str, Any]): 
            The data associated with the section, which can include analysis results, metrics, etc.
        chart (Dict[str, Any]): 
            The chart information for the section, which can include the chart type, 
            data for plotting, and any relevant metadata.
    """
    data: Dict[str, Any]
    chart: Dict[str, Any]


class ReportBuilder:
    """
    Class to build a comprehensive EDA report with multiple sections, including both textual data and charts.
    Attributes:
        df (pd.DataFrame): The input DataFrame containing the data to be analyzed.
        target_col (str): The name of the target column in the DataFrame for analysis.
        date_col (str): The name of the date column in the DataFrame for time series analysis.
        config (ConfigBuilder): An instance of ConfigBuilder to manage configuration settings for the report.
        sections (OrderedDict[str, SectionContent]): An ordered dictionary to store the sections of the report, 
            where keys are section names and values are SectionContent instances containing data and chart information.
    Methods:
        add_section(name: str, data: Dict[str, Any], chart: Optional[Dict[str, Any]] = None) -> Self:
            Adds a section to the report with the given name, data, and optional chart information.
        add_section_by_name(name: str) -> Self:
            Adds a section to the report by looking up a registered section builder function by name and executing it.
        build(output_path: Optional[str] = None) -> Dict[str, Any]:
            Builds the report data structure, which can be output as JSON or used for further processing.
        image_to_base64(image_path: str) -> str:
            Converts an image file to a base64 string for embedding in HTML or JSON.
        save(outfile_name: Optional[str] = None) -> None:
            Saves the generated report as a JSON file with the specified name.
    """
    def __init__(self, df: pd.DataFrame, target_col: str, date_col: str, config: ConfigBuilder = ConfigBuilder):
        """Initializes the ReportBuilder with the provided DataFrame, target column, date column, and configuration builder."""
        self.df = df.copy(deep=True)
        self.target_col = target_col
        self.date_col = date_col
        self.config = self._config()
        self.sections: OrderedDict[str, SectionContent] = OrderedDict()
        self._report_data: Optional[Dict[str, Any]] = None
        self._added_sections: List[str] = []  # To track which sections have been added to avoid duplicates

    def _config(self) -> ConfigBuilder:
        """Initializes and returns a ConfigBuilder instance based on the current DataFrame, target column, and date column."""
        return ConfigBuilder(
            df=self.df.copy(deep=True),
            target_col=self.target_col,
            date_col=self.date_col,
        )

    def add_all_sections(self, verbose: bool = False) -> Self:
        """Adds all registered sections to the report by iterating through the 
        SECTION_BUILDERS registry and adding each section by name."""
        for section_name in SECTION_BUILDERS.keys():
            self.add_section_by_name(section_name)
            self._added_sections.append(section_name)
            if verbose:
                print(f"Added section: {section_name}")
        return self

    def include_sections(self, section_names: list[Union[str, SectionEnum]], verbose: bool = False) -> Self:
        """
        Keep only the specified sections in the report.
        Args:
            section_names (list[Union[str, SectionEnum]]): List of section names or SectionEnum members to include.
            verbose (bool): If True, prints the names of the sections being included.
        """
        include_names = [s.value if isinstance(s, SectionEnum) else s for s in section_names]
        for section_name in SECTION_BUILDERS.keys():
            if section_name in include_names:
                self.add_section_by_name(section_name)
                self._added_sections.append(section_name)
                if verbose:
                    print(f"Included section: {section_name}")
        self._report_data = None  # Invalidate cache if needed
        return self

    def exclude_sections(self, section_names: list[Union[str, SectionEnum]], verbose: bool = False) -> Self:
        """
        Excludes specified sections from the report by removing them from the sections dictionary.
        Args:            
            section_names (list[Union[str, SectionEnum]]): 
                A list of section names or SectionEnum members to be excluded from the report.
            verbose (bool): 
                If True, prints the names of the sections being excluded.
        """
        exclude_sections = [s.value if isinstance(s, SectionEnum) else s for s in section_names]
        include_sections = [s for s in SECTION_BUILDERS.keys() if s not in exclude_sections]   
        for section_name in SECTION_BUILDERS.keys():
            if section_name in include_sections:
                self.add_section_by_name(section_name)
                self._added_sections.append(section_name)
                if verbose:
                    print(f"Included section: {section_name}")
        self._report_data = None  # Invalidate cache if needed
        return self

    def add_section(self, name: str, data: Dict[str, Any], chart: Optional[Dict[str, Any]] = None) -> Self:
        """
        Adds a section to the report with the given name, data, and optional chart information.
        Args:
            name (str): The name of the section to add.
            data (Dict[str, Any]): The data associated with the section.
            chart (Optional[Dict[str, Any]]): The chart information for the section.
        Returns:
            Self: The current instance of the ReportBuilder.
        """
        self.sections[name] = SectionContent(data=data, chart=chart or {})
        return self

    def add_section_by_name(self, name: str, verbose: bool = False) -> Self:
        """
        Adds a section to the report by looking up a registered section builder function by name and executing it.
        Args:
            name (str): The name of the section to add.
            verbose (bool): If True, prints the name of the section being added.
        Returns:
            Self: The current instance of the ReportBuilder.
        Raises:
            ValueError: If no section builder is registered for the given name.
        """
        builder = SECTION_BUILDERS.get(name)
        if not builder:
            raise ValueError(f"No section builder registered for {name}")
        section = builder(self)
        self.add_section(name=name, data=section["data"], chart=section.get("chart"))
        if verbose:
            print(f"Added section: {name}")
        self._added_sections.append(name)
        return self

    def build(self, output_path: Optional[str] = None, with_all_sections: bool = False, verbose: bool = False) -> Dict[str, Any]:
        """
        Builds the report data structure, which can be output as JSON or used for further processing.
        Args:
            output_path (Optional[str]): The path where the report should be saved as a JSON file. If None, the report is not saved to a file.
            with_all_sections (bool): If True, includes all sections in the report, even if they were not explicitly added.
            verbose (bool): If True, prints additional information during the build process.
        Returns:
            Dict[str, Any]: A dictionary representing the report data, including sections and their associated data and charts.
        """
        if verbose:
            print("Building report...")
            if not with_all_sections and not self._added_sections:
                print(
                    "No sections have been added to the report. "
                    "Use either add_all_sections(), include_sections(), or add_section_by_name() "
                    "to add sections before building the report.\n"
                    "Or set with_all_sections=True to include all registered sections in the report."
                )
        if with_all_sections and not self._added_sections:
            self.add_all_sections(verbose=verbose)
        if self._report_data is not None:
            return self._report_data  # Return cached report data if already built
        report_data = {
            "sections": {
                section_name: {
                    "data": content.data,
                    "chart": content.chart
                }
                for section_name, content in self.sections.items()
            }
        }
        self._report_data = report_data  # Cache the built report data for potential reuse
        return report_data

    def image_to_base64(self, image_path: str) -> str:
        """
        Convert an image file to a base64 string for embedding in HTML.
        Args:
            image_path (str): Path to the image file.
        Returns:
            str: Base64-encoded image string with MIME type, or empty string if not found.
        """
        if not os.path.exists(image_path):
            print(f"Warning: Image file {image_path} not found.")
            return ""

        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

            ext = os.path.splitext(image_path)[1].lower()
            mime_types = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".gif": "image/gif",
                ".webp": "image/webp",
            }
            mime_type = mime_types.get(ext, "image/png")
            return f"data:{mime_type};base64,{encoded_string}"

    def save(self, outfile_name: Optional[str] = None) -> None:
        """
        Save the generated report as a JSON file.
        Args:
            outfile_name (Optional[str]): The name of the output JSON file. If None, defaults to "report.json".
        """
        # Check if the report data has already been built; if not, build it before saving
        if self._report_data is None:
            self.build(verbose=True)
        report_data = self._report_data
        outfile_name = outfile_name or DEFAULT_OUTJSON_FILENAME
        output_path = os.path.join(self.config.output_dir, outfile_name)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, mode="w") as f:
            json.dump(report_data, f, indent=2)
