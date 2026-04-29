# owlmix/report/generator.py
"""
Report Generation Orchestrator Module

This module serves as the primary high-level interface for the OwlMix EDA
reporting system. It coordinates the data analysis process and the final
rendering of results.

The `OwlMixReport` class manages the end-to-end workflow:
1.  **Initialization**: Configures data schemas and output directories.
2.  **Analysis**: Leverages `SummaryBuilder` to perform statistical calculations
    (VIF, ACF/PACF, correlations) and generate visualization assets.
3.  **JSON Export**: Serializes the raw analysis results for data persistence.
4.  **HTML Rendering**: Hands off the processed data and chart paths to
    `HTMLRenderer` to produce a finalized, interactive browser report.

This module is designed to be the main entry point for users looking to
generate comprehensive Exploratory Data Analysis reports for MMM projects.
"""

import os
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from typing import Self, TypedDict, Unpack, NotRequired

from owlmix.eda.summary import SummaryBuilder
from owlmix.report.renderer import HTMLRenderer
from owlmix.eda.summary_builder_config import SummaryBuilderConfig


@dataclass
class ReportSettings:  # Renamed from ReportConfig to avoid conflict
    """Configuration for report generation."""
    output_dir: str = "outputs"
    template_name: str = "report.html"
    template_path: str | None = None
    json_file_name: str = "report.json"
    html_file_name: str = "report.html"


class UserTitleConfig(TypedDict):
    user_title_config_path: NotRequired[str]


class OwlMixReport:

    def __init__(self, df: pd.DataFrame, target: str, date_column: str, report_settings: ReportSettings | None = None, **kwargs: Unpack[UserTitleConfig]):
        """
        Initialize OwlMixReport class.

        Args:
            df: Input DataFrame
            target: Target column name
            date_column: Date column name
            report_settings: ReportSettings instance (optional, will be created from kwargs if not provided)
            **kwargs: Fallback config values (output_dir, template_name, template_path, etc.)
        """
        self.df = df
        self.target = target
        self.date_column = date_column
        self.user_title_config_path = self._get_user_title_config_path(kwargs)

        # Use provided settings or create from kwargs
        self.report_settings = report_settings or self._create_settings_from_kwargs(**kwargs)
        self.chart_dir = os.path.join(self.report_settings.output_dir, "charts")

        self._initialize_directories()
        self.config = self._get_summary_builder_config()
        self.summary_builder = self._get_summary_builder()

    def _get_summary_builder(self) -> SummaryBuilder:
        return SummaryBuilder(
            self.df,
            target=self.target,
            date_column=self.date_column,
            output_dir=self.chart_dir,
            config=self.config,
            user_title_config_path=self.user_title_config_path
        )

    def _get_summary_builder_config(self) -> SummaryBuilderConfig:
        return SummaryBuilderConfig(
            df=self.df,
            target=self.target,
            date_column=self.date_column
        )

    def _get_user_title_config_path(self, kwargs) -> Path | None:
        kwarg_name: str = "user_title_config_path"
        if kwargs.get(kwarg_name, None) is not None:
            return Path(kwargs.get(kwarg_name, None)).resolve()
        return None

    def _create_settings_from_kwargs(self, **kwargs) -> ReportSettings:
        """Create ReportSettings from kwargs with sensible defaults."""
        return ReportSettings(
            output_dir=kwargs.get("output_dir", "outputs"),
            template_name=kwargs.get("template_name", "report.html"),
            template_path=kwargs.get("template_path"),
            json_file_name=kwargs.get("json_file_name", "report.json"),
            html_file_name=kwargs.get("html_file_name", "report.html"),
        )

    def _initialize_directories(self) -> None:
        """Create necessary output directories."""
        os.makedirs(self.chart_dir, exist_ok=True)

    def generate_json(self, out_file_name: str | None = None) -> tuple[dict, str]:
        """
        Generate JSON report.

        Returns:
            Tuple of (report_dict, json_path)
        """
        out_file_name = out_file_name or self.report_settings.json_file_name

        builder = self.summary_builder.add_all()
        report_dict = builder.build()

        json_path = os.path.join(self.report_settings.output_dir, out_file_name)
        builder.save(json_path)

        return report_dict, json_path

    def generate_html(self, out_file_name: str | None = None) -> str:
        """
        Generate HTML report.

        Args:
            out_file_name: Custom output filename (uses default if not provided)

        Returns:
            Path to generated HTML file
        """
        out_file_name = out_file_name or self.report_settings.html_file_name
        html_output_path = os.path.join(self.report_settings.output_dir, out_file_name)

        report_dict, _ = self.generate_json()

        renderer = HTMLRenderer(
            template_name=self.report_settings.template_name,
            template_path=self.report_settings.template_path
        )

        renderer.render(report_dict, html_output_path)
        return html_output_path

    def run(self, json_file_name: str | None = None, html_file_name: str | None = None) -> None:
        """
        Generate both JSON and HTML reports.

        Args:
            json_file_name: Custom JSON output filename
            html_file_name: Custom HTML output filename
        """
        if json_file_name:
            self.report_settings.json_file_name = json_file_name
        if html_file_name:
            self.report_settings.html_file_name = html_file_name

        self.generate_html(out_file_name=html_file_name)


if "__main__" == __name__:
    OwlMixReport(
        df=pd.read_csv(),
        target="target",
        date_column="date",
        user_title_config_path="user_title_config_path",
    )