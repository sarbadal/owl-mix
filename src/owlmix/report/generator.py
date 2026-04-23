# src/owlmix/report/generator.py
import os
from typing import TypedDict, NotRequired
from dataclasses import dataclass

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


class OwlMixReport:

    def __init__(self, df: "pd.DataFrame", target: str, date_column: str, report_settings: ReportSettings | None = None, **kwargs):
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

        # Use provided settings or create from kwargs
        self.report_settings = report_settings or self._create_settings_from_kwargs(**kwargs)
        self.chart_dir = os.path.join(self.report_settings.output_dir, "charts")

        self._initialize_directories()
        self.config = SummaryBuilderConfig(
            df=self.df,
            target=self.target,
            date_column=self.date_column
        )

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

    def _apply_builder_configs(self, builder: SummaryBuilder) -> None:
        """Apply all configuration settings to builder."""
        config_methods = [
            ("set_time_comparison_config", self.config.time_comparison_config),
            ("set_vif_config", self.config.vif_config),
            ("set_kpi_vs_feature_config", self.config.kpi_vs_feature_config),
            ("set_acf_pacf_config", self.config.acf_pacf_config),
            ("set_categorical_columns_config", self.config.categorical_columns_config),
            ("set_correlation_config", self.config.correlation_config),
            ("set_outlier_chart_layout_config", self.config.outlier_chart_layout_config),
            ("set_correlation_chart_layout_config", self.config.correlation_chart_layout_config),
        ]

        for method_name, config_value in config_methods:
            getattr(builder.config, method_name)(**config_value)

    def generate_json(self, out_file_name: str | None = None) -> tuple[dict, str]:
        """
        Generate JSON report.

        Returns:
            Tuple of (report_dict, json_path)
        """
        out_file_name = out_file_name or self.report_settings.json_file_name

        builder = SummaryBuilder(
            self.df,
            target=self.target,
            date_column=self.date_column,
            output_dir=self.chart_dir,
            config=self.config
        )

        self._apply_builder_configs(builder)

        builder = builder.add_all()
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