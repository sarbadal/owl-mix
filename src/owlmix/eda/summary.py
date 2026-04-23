# src/owlmix/eda/summary.py
import os
import base64
from typing import Self

import pandas as pd
import json

from owlmix.eda import kpi_vs_feature
from owlmix.eda.basic import get_basic_info
from owlmix.eda.correlation import get_correlation_matrix, get_lag_correlation

from owlmix.eda.basic import BasicInfo
from owlmix.eda.stats import BasicStats
from owlmix.eda.correlation import Correlation
from owlmix.eda.vif import VIFCalculator
from owlmix.eda.acf_pacf import ACFPACFCalculator
from owlmix.eda.time.comparison import TimeComparisonReport, TimeAggregatorReport
from owlmix.eda.causality import CausalityTest
from owlmix.eda.categorical_distribution_generator import CategoricalDistributionGenerator
from owlmix.eda.kpi_vs_feature import DualAxisLineChartDataGenerator

from owlmix.eda.charts.time.comparison import ComparisonChart
from owlmix.eda.charts.correlation import CorrelationChart
from owlmix.eda.charts.time_series import TimeSeriesChart
from owlmix.eda.charts.outliers import OutlierChart
from owlmix.eda.charts.lag import LagCorrelationChart
from owlmix.eda.charts.distribution import DistributionChart
from owlmix.eda.charts.categorical_distribution import CategoricalDistributionChart
from owlmix.eda.charts.vif import VIFChart
from owlmix.eda.charts.dualaxis_line_plot import DualAxisLinePlotter
from owlmix.eda.charts.acf_pacf import ACFPACFPlotter

from owlmix.eda.summary_builder_config import SummaryBuilderConfig

from .config_model import ChartsTitleConfig, build_charts_config


class SummaryBuilder:
    def __init__(
            self,
            df: pd.DataFrame,
            target: str,
            date_column: str,
            output_dir: str = "eda_output",
            config: SummaryBuilderConfig = None,
            user_title_config_path: str = None
    ):
        self.df = df
        self.target = target
        self.date_column = date_column
        self.output_dir = output_dir

        self.sections = []
        self.chart_paths = []
        self.config = config
        self.title_config = build_charts_config(user_title_config_path)

        # Internal cache for intermediate data (consolidates _dual_axis_chart_data, etc.)
        self._chart_data_cache = {
            "dual_axis": None,
            "acf_pacf": None,
            "categorical": None,
        }

        os.makedirs(self.output_dir, exist_ok=True)

    # =========================
    # PRIVATE HELPER METHODS
    # =========================

    def _get_config_value(self, config_dict: dict, key: str, fallback=None):
        """Safely retrieve a configuration value with optional fallback."""
        return config_dict.get(key, fallback)

    def _add_section(self, section_key: str, section_value) -> None:
        """Add a section to the report in a consistent manner."""
        self.sections.append({section_key: section_value})

    def _append_chart(self, chart_id: str, path: str) -> None:
        """Append a chart with metadata to chart_paths."""
        title = self.title_config.charts[chart_id].title
        description = self.title_config.charts[chart_id].description
        alt_text = self.title_config.charts[chart_id].alt_text

        self.chart_paths.append({
            "title": title,
            "description": description,
            chart_id: path,
            "image_data": self._image_to_base64(path),
            "alt_text": alt_text
        })

    # =========================
    # TEXT SECTIONS - Basic Info & Correlations
    # =========================

    def add_basic_info(self):
        basic = BasicInfo(self.df)
        json_content = basic.to_json()
        self._add_section("basic_info", json.loads(json_content))
        return self

    def add_correlation_matrix(self) -> Self:
        columns = self.config.correlation_config["columns"]
        corr = Correlation(df=self.df, columns=columns)

        self._add_section("correlation_matrix", corr.compute_correlation_matrix())
        self._add_section(
            "lag_correlation",
            corr.compute_lag_correlation(self.target, self.target, lags=[1, 2, 3, 4, 5])
        )
        return self

    # ===================================
    # TEXT SECTIONS - VIF & KPI Analysis
    # ===================================

    def add_vif_calculator(self) -> Self:
        config = self.config.vif_config

        vif_calculator = VIFCalculator(
            df=self.df,
            target_column=config["target_column"],
            features=config["features"],
            precision=config["precision"],
        )
        self._add_section("vif", vif_calculator.compute_vif())
        return self

    def add_kpi_vs_feature(self) -> Self:
        config = self.config.kpi_vs_feature_config

        kpi_vs_feature_generator = DualAxisLineChartDataGenerator(
            df=self.df,
            target_column=config["target_column"],
            columns=config["columns"],
            date_format=config["date_format"],
            date_column=config["date_column"],
            agg_func=config["agg_func"],
        )
        result = kpi_vs_feature_generator.generate()
        self._add_section("kpi_vs_features", result)
        self._chart_data_cache["dual_axis"] = result["data"]
        return self

    # =============================
    # TEXT SECTIONS - Time Analysis
    # =============================

    def add_time_comparison(self) -> Self:
        config = self.config.time_comparison_config
        report = TimeComparisonReport(
            df=self.df,
            date_column=config["date_column"],
            value_columns=config["value_columns"],
            comparison_type=config["comparison_type"],
            agg_func=config["agg_func"],
            precision=config["precision"]
        )
        self._add_section("time_comparison", report.generate())
        return self

    def add_time_aggregator(self) -> Self:
        config = self.config.time_aggregator_config
        report = TimeAggregatorReport(
            df=self.df,
            date_column=config["date_column"],
            value_columns=config["value_columns"],
            freq=config["freq"],
            agg_func=config["agg_func"],
            precision=config["precision"]
        )
        self._add_section("time_aggregator", report.aggregate())
        return self

    # =================================
    # TEXT SECTIONS - Advanced Analysis
    # =================================

    def add_causality_test(self) -> Self:
        config = self.config.causality_test_config
        causality_test = CausalityTest(
            df=self.df,
            target_column=config["target_column"],
            columns=config["columns"]
        )
        result = causality_test.run(
            max_lag=config["max_lag"],
            error_threshold=config["error_threshold"]
        )
        self._add_section("causality_test", result)
        return self

    def add_categorical_distribution(self) -> Self:
        columns = self.config.categorical_columns_config["columns"]
        generator = CategoricalDistributionGenerator(df=self.df, columns=columns)
        result = generator.generate()

        self._add_section("categorical_distribution", result)
        self._chart_data_cache["categorical"] = result["data"]
        return self

    def add_acf_pacf_calculator(self) -> Self:
        config = self.config.acf_pacf_config

        generator = ACFPACFCalculator(
            df=self.df,
            columns=config["columns"],
            n_lags=config["n_lags"],
        )
        result = generator.generate()

        self._add_section("acf_pacf", result)
        self._chart_data_cache["acf_pacf"] = result["data"]
        return self

    # ================================
    # CHART SECTIONS - Standard Charts
    # ================================

    def add_distribution_chart(self) -> Self:
        columns = self.config.correlation_config["columns"]
        chart = DistributionChart(
            df=self.df,
            columns=columns,
            output_dir=self.output_dir
        )
        self._append_chart("distribution_chart", chart.generate())
        return self

    def add_correlation_chart(self):
        config = self.config.correlation_chart_layout_config
        chart = CorrelationChart(
            df=self.df,
            columns=config["columns"],
            precision=config["precision"],
            output_dir=self.output_dir
        )
        self._append_chart("correlation_chart", chart.generate())
        return self

    def add_time_series_chart(self, columns=None):
        columns = self.config.time_series_config["columns"]
        chart = TimeSeriesChart(
            self.df,
            columns=columns,
            target=self.target,
            date_column=self.date_column,
            output_dir=self.output_dir
        )
        self._append_chart("time_series_chart", chart.generate())
        return self

    def add_outliers_chart(self):
        config = self.config.outlier_chart_layout_config
        chart = OutlierChart(
            df=self.df,
            columns=config["columns"],
            max_cols_per_chart=config["max_cols_per_chart"],
            single_image=config["single_image"],
            output_dir=self.output_dir
        )
        self._append_chart("outliers_chart", chart.generate())
        return self

    # ================================
    # CHART SECTIONS - Analysis Charts
    # ================================

    def add_vif_chart(self) -> Self:
        config = self.config.vif_config
        chart = VIFChart(
            df=self.df,
            target_column=config["target_column"],
            features=config["features"],
            precision=config["precision"],
            output_dir=self.output_dir
        )
        self._append_chart("vif_chart", chart.generate())
        return self

    def add_comparison_chart(self) -> Self:
        config = self.config.time_comparison_config
        chart = ComparisonChart(
            df=self.df,
            date_column=config["date_column"],
            value_columns=config["value_columns"],
            freq=config.get("freq", "D"),
            comparison=config.get("comparison", "yoy"),
            output_dir=self.output_dir,
        )
        self._append_chart("comparison_chart", chart.generate())
        return self

    def add_lag_correlation_chart(self, lag=1):
        chart = LagCorrelationChart(
            df=self.df,
            column=self.target,
            output_dir=self.output_dir,
            lag=lag
        )
        self._append_chart("lag_correlation_chart", chart.generate())
        return self

    # ===================================
    # CHART SECTIONS - Data-Driven Charts
    # ===================================

    def add_acf_pacf_chart(self) -> Self:
        data = self._chart_data_cache.get("acf_pacf")
        if data is None:
            return self

        chart = ACFPACFPlotter(data=data, output_dir=self.output_dir)
        path = chart.generate()

        if path is not None:
            self._append_chart("acf_pacf_chart", path)
        return self

    def add_kpi_vs_feature_chart(self) -> Self:
        data = self._chart_data_cache.get("dual_axis")
        if data is None:
            return self

        chart = DualAxisLinePlotter(data=data, output_dir=self.output_dir)
        path = chart.generate()

        if path is not None:
            self._append_chart("kpi_vs_feature_chart", path)
        return self

    def add_categorical_distribution_chart(self) -> Self:
        if not self.config.categorical_columns_config["columns"]:
            return self

        data = self._chart_data_cache.get("categorical")
        if data is None:
            return self

        chart = CategoricalDistributionChart(data=data, output_dir=self.output_dir)
        path = chart.generate()

        if path is not None:
            self._append_chart("categorical_distribution_chart", path)
        return self

    # =========================
    # METADATA SECTIONS
    # =========================

    def add_report_title(self, title: str = "OwlMix EDA Report"):
        self._add_section("title", title)
        return self

    def add_header_title(self, title: str = "🦉 OwlMix EDA Report"):
        self._add_section("header_title", title)
        return self

    def add_header_subtitle(self, subtitle: str = None):
        subtitle = subtitle or "Exploratory Data Analysis for Marketing Mix Modeling"
        self._add_section("header_subtitle", subtitle)
        return self

    def add_columns_as_list(self):
        self._add_section("columns", self.df.columns.tolist())
        return self

    def add_footer(self, text: str = "Generated by OwlMix EDA"):
        self._add_section("generator", text)
        self._add_section("report_date", pd.Timestamp.now().isoformat())
        return self

    # =========================
    # BUILD ALL SECTIONS
    # =========================

    def add_all(self):
        """Add all default sections to the report."""
        return (
            self
            .add_report_title()
            .add_header_title()
            .add_header_subtitle()
            .add_columns_as_list()
            .add_footer()
            .add_basic_info()
            .add_correlation_matrix()
            .add_correlation_chart()
            .add_vif_calculator()
            .add_kpi_vs_feature()
            .add_acf_pacf_calculator()
            .add_causality_test()
            .add_categorical_distribution()
            .add_time_aggregator()
            .add_time_comparison()
            .add_time_series_chart()
            .add_kpi_vs_feature_chart()
            .add_outliers_chart()
            .add_lag_correlation_chart()
            .add_comparison_chart()
            .add_vif_chart()
            .add_acf_pacf_chart()
            .add_distribution_chart()
            .add_categorical_distribution_chart()
        )

    # =========================
    # OUTPUT METHODS
    # =========================

    def build(self) -> dict:
        """Build the final report dictionary."""
        return {
            "sections": self.sections,
            "charts": self.chart_paths
        }

    def save(self, filename: str = "eda_report.json"):
        """Save the report to a JSON file."""
        result = self.build()
        if os.path.dirname(filename):
            file_path = filename
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        else:
            file_path = os.path.join(self.output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

    def _image_to_base64(self, image_path: str) -> str:
        """Convert an image file to a base64 string for embedding in HTML."""
        if not os.path.exists(image_path):
            print(f"Warning: Image file {image_path} not found.")
            return ""

        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            # Get file extension to determine MIME type
            ext = os.path.splitext(image_path)[1].lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp',
            }
            mime_type = mime_types.get(ext, 'image/png')

            return f'data:{mime_type};base64,{encoded_string}'
