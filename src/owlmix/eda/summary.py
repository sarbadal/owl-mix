# owlmix/eda/summary.py
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
from typing import Any, Self, Callable, Optional, Dict, List, Set
from collections import OrderedDict

from . import (
    BasicInfo,
    BasicStats,
    Correlation,
    VIFCalculator,
    ACFPACFCalculator,
    TimeComparisonReport,
    CausalityTest,
    CategoricalDistributionGenerator,
    DualAxisLineChartDataGenerator,
)

from .charts import (
    ComparisonChart,
    CorrelationChart,
    TimeSeriesChart,
    OutlierChart,
    LagCorrelationChart,
    DistributionChart,
    CategoricalDistributionChart,
    VIFChart,
    DualAxisLinePlotter,
    ACFPACFPlotter,
)

from .summary_builder_config import SummaryBuilderConfig
from .config_model import ChartsTitleConfig, build_charts_config
from ..typing.enums import ChartID


class SummaryBuilder:
    """
    Builds and manages the generation of EDA (Exploratory Data Analysis) reports.

    This class provides a flexible API to add various sections and charts to an EDA report,
    configure which charts to include/exclude, and output the report as a JSON file.

    Attributes:
        df (pd.DataFrame): The input dataframe for analysis.
        target (str): The target column for analysis.
        date_column (str): The column representing dates.
        output_dir (str): Directory to save output files.
        config (SummaryBuilderConfig): Configuration for report sections and charts.
        title_config (ChartsTitleConfig): Chart title and description configuration.
        sections (List[dict]): List of report sections.
        chart_paths (List[dict]): List of chart metadata and paths.
        _chart_data_cache (Dict[str, Any]): Internal cache for intermediate chart data.
        _charts (Dict[ChartID, Callable]): Mapping of chart IDs to chart-adding methods.
        _non_charts (Dict[str, Callable]): Mapping of section names to non-chart methods.
        _include (Optional[Set[ChartID]]): Set of chart IDs to include.
        _exclude (Set[ChartID]): Set of chart IDs to exclude.
        _custom_order (Optional[List[ChartID]]): Custom order for charts.
    """

    def __init__(
        self, df: pd.DataFrame, target: str, date_column: str, output_dir: str = "outputs", config: Optional[SummaryBuilderConfig] = None, user_title_config_path: Optional[str] = None):
        """
        Initialize the SummaryBuilder.

        Args:
            df (pd.DataFrame): The dataframe to analyze.
            target (str): The target column for analysis.
            date_column (str): The column containing date information.
            output_dir (str, optional): Directory to save outputs. Defaults to "eda_output".
            config (SummaryBuilderConfig, optional): Configuration object for the report.
            user_title_config_path (str, optional): Path to user-defined chart titles.
        """
        self.df: pd.DataFrame = df
        self.target: str = target
        self.date_column: str = date_column
        self.output_dir: str = output_dir

        self.sections: List[dict] = []
        self.chart_paths: List[dict] = []
        self.config: Optional[SummaryBuilderConfig] = config
        self.title_config: ChartsTitleConfig = build_charts_config(user_title_config_path)

        self._chart_data_cache: Dict[str, Any] = {
            "dual_axis": None,
            "acf_pacf": None,
            "categorical": None,
        }

        self._charts: Dict[ChartID, Callable[[], Self]] = OrderedDict([
            (ChartID.DISTRIBUTION_CHART, self.add_distribution_chart),
            (ChartID.CORRELATION_CHART, self.add_correlation_chart),
            (ChartID.TIME_SERIES_CHART, self.add_time_series_chart),
            (ChartID.OUTLIERS_CHART, self.add_outliers_chart),
            (ChartID.VIF_CHART, self.add_vif_chart),
            (ChartID.COMPARISON_CHART, self.add_time_comparison_chart),
            (ChartID.LAG_CORRELATION_CHART, self.add_lag_correlation_chart),
            (ChartID.ACF_PACF_CHART, self.add_acf_pacf_chart),
            (ChartID.KPI_VS_FEATURE_CHART, self.add_kpi_vs_feature_chart),
            (ChartID.CATEGORICAL_DISTRIBUTION_CHART, self.add_categorical_distribution_chart)
        ])

        self._non_charts: Dict[str, Callable[[], Self]] = {
            "report_title": self.add_report_title,
            "header_title": self.add_header_title,
            "header_subtitle": self.add_header_subtitle,
            "columns_as_list": self.add_columns_as_list,
            "footer": self.add_footer,
            "basic_info": self.add_basic_info,
            "correlation_matrix": self.add_correlation_matrix,
            "vif_calculator": self.add_vif_calculator,
            "kpi_vs_feature": self.add_kpi_vs_feature,
            "acf_pacf_calculator": self.add_acf_pacf_calculator,
            "causality_test": self.add_causality_test,
            "time_comparison": self.add_time_comparison,
            "categorical_distribution": self.add_categorical_distribution,
        }

        self._include: Optional[Set[ChartID]] = None
        self._exclude: Set[ChartID] = set()
        self._custom_order: Optional[List[ChartID]] = None

        os.makedirs(self.output_dir, exist_ok=True)

    def include_charts(self, *chart_ids: ChartID) -> Self:
        """
        Specify which charts to include in the report.

        Args:
            *chart_ids (ChartID): Chart IDs to include.

        Returns:
            Self: The current instance for method chaining.
        """
        self._include = {c for c in chart_ids}
        return self

    def exclude_charts(self, *chart_ids: ChartID) -> Self:
        """
        Specify which charts to exclude from the report.

        Args:
            *chart_ids (ChartID): Chart IDs to exclude.

        Returns:
            Self: The current instance for method chaining.
        """
        self._exclude = {c for c in chart_ids}
        return self

    def reorder_charts(self, *chart_ids: ChartID) -> Self:
        """
        Specify a custom order for charts in the report. Partial order is allowed.

        Args:
            *chart_ids (ChartID): Chart IDs in desired order.

        Returns:
            Self: The current instance for method chaining.

        Raises:
            ValueError: If no chart IDs are provided or invalid IDs are given.
        """
        if not chart_ids:
            raise ValueError("At least one chart_id must be provided")

        seen: Set[ChartID] = set()
        ordered: List[ChartID] = []
        for cid in chart_ids:
            if cid not in seen:
                seen.add(cid)
                ordered.append(cid)

        self._custom_order = ordered
        return self

    def _resolve_charts(self) -> List[ChartID]:
        """
        Resolve the list of charts to include in the report, considering include/exclude and custom order.

        Returns:
            List[ChartID]: Ordered list of chart IDs to include.

        Raises:
            KeyError: If invalid chart IDs are specified.
            ValueError: If invalid chart IDs are specified in custom order.
        """
        all_charts: List[ChartID] = list(self._charts.keys())

        if self._include is not None:
            invalid = self._include - set(all_charts)
            if invalid:
                raise KeyError(f"Invalid chart IDs in include: {invalid}")
            filtered = [cid for cid in all_charts if cid in self._include]
        else:
            invalid = self._exclude - set(all_charts)
            if invalid:
                raise KeyError(f"Invalid chart IDs in exclude: {invalid}")
            filtered = [cid for cid in all_charts if cid not in self._exclude]

        if self._custom_order is None:
            return filtered

        invalid = set(self._custom_order) - set(all_charts)
        if invalid:
            raise ValueError(f"Invalid chart IDs in reorder: {invalid}")

        custom = [cid for cid in self._custom_order if cid in filtered]
        remaining = [cid for cid in filtered if cid not in custom]

        return custom + remaining

    def _get_config_value(self, config_dict: dict, key: str, fallback: Any = None) -> Any:
        """
        Safely retrieve a configuration value with optional fallback.

        Args:
            config_dict (dict): Configuration dictionary.
            key (str): Key to retrieve.
            fallback (Any, optional): Fallback value if key is missing.

        Returns:
            Any: The configuration value or fallback.
        """
        return config_dict.get(key, fallback)

    def _add_section(self, section_key: str, section_value: Any) -> None:
        """
        Internal helper to add a section to the report.

        Args:
            section_key (str): The key/name of the section.
            section_value (Any): The content/value of the section.
        """
        self.sections.append({section_key: section_value})

    def _append_chart(self, chart_id: str, path: str) -> None:
        """
        Append a chart with metadata to chart_paths.

        Args:
            chart_id (str): The chart identifier.
            path (str): Path to the chart image file.
        """
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

    def add_basic_info(self) -> Self:
        """
        Add basic information about the dataframe to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        basic = BasicInfo(self.df)
        json_content = basic.to_json()
        self._add_section("basic_info", json.loads(json_content))
        return self

    def add_correlation_matrix(self) -> Self:
        """
        Add correlation matrix and lagged correlations to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        columns = self.config.correlation_config.columns
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
        """
        Add Variance Inflation Factor (VIF) analysis to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        config = self.config.vif_config

        vif_calculator = VIFCalculator(
            df=self.df,
            target_column=config.target_column,
            features=config.features,
            precision=config.precision,
            color_thresholds=config.color_thresholds,
        )
        self._add_section("vif", vif_calculator.compute_vif())
        return self

    def add_kpi_vs_feature(self) -> Self:
        """
        Add KPI vs. feature analysis to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        config = self.config.kpi_vs_feature_config
        kpi_vs_feature_generator = DualAxisLineChartDataGenerator(
            df=self.df,
            target_column=config.target_column,
            columns=config.columns,
            period=config.period,
            date_column=config.date_column,
            agg_func=config.agg_func,
        )
        result = kpi_vs_feature_generator.generate()
        self._add_section("kpi_vs_features", result)
        self._chart_data_cache["dual_axis"] = result["data"]
        return self

    # =============================
    # TEXT SECTIONS - Time Analysis
    # =============================

    def add_time_comparison(self) -> Self:
        """
        Add time comparison analysis to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        config = self.config.time_comparison_config
        report = TimeComparisonReport(
            df=self.df,
            date_column=config.date_column,
            value_columns=config.value_columns,
            comparison_type=config.comparison_type,
            agg_func=config.agg_func,
            precision=config.precision
        )
        self._add_section("time_comparison", report.generate())
        return self

    # =================================
    # TEXT SECTIONS - Advanced Analysis
    # =================================

    def add_causality_test(self) -> Self:
        """
        Add causality test results to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        config = self.config.causality_test_config
        causality_test = CausalityTest(
            df=self.df,
            target_column=config.target_column,  # config["target_column"],
            columns=config.columns  # config["columns"]
        )
        result = causality_test.run(
            max_lag=config.max_lag,  # config["max_lag"],
            error_threshold=config.error_threshold  # config["error_threshold"]
        )
        self._add_section("causality_test", result)
        return self

    def add_categorical_distribution(self) -> Self:
        """
        Add categorical distribution analysis to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        config = self.config.categorical_columns_config
        generator = CategoricalDistributionGenerator(
            df=self.df, 
            columns=config.columns
        )
        result = generator.generate()

        self._add_section("categorical_distribution", result)
        self._chart_data_cache["categorical"] = result["data"]
        return self

    def add_acf_pacf_calculator(self) -> Self:
        """
        Add ACF/PACF analysis to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        config = self.config.acf_pacf_config
        generator = ACFPACFCalculator(
            df=self.df,
            columns= config.columns, 
            n_lags=config.n_lags, 
        )
        result = generator.generate()

        self._add_section("acf_pacf", result)
        self._chart_data_cache["acf_pacf"] = result["data"]
        return self

    # ================================
    # CHART SECTIONS - Standard Charts
    # ================================

    def add_distribution_chart(self) -> Self:
        """
        Add a distribution chart to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        columns = self.config.distribution_chart_config.columns
        chart = DistributionChart(
            df=self.df,
            columns=columns,
            output_dir=self.output_dir
        )
        self._append_chart("distribution_chart", chart.generate())
        return self

    def add_correlation_chart(self) -> Self:
        """
        Add a correlation chart to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        config = self.config.correlation_chart_layout_config
        chart = CorrelationChart(
            df=self.df,
            columns=config.columns,
            precision=config.precision,
            output_dir=self.output_dir
        )
        self._append_chart("correlation_chart", chart.generate())
        return self

    def add_time_series_chart(self, columns: Optional[List[str]] = None) -> Self:
        """
        Add a time series chart to the report.

        Args:
            columns (Optional[List[str]], optional): Columns to include. Defaults to config.

        Returns:
            Self: The current instance for method chaining.
        """
        columns = self.config.time_series_config.columns
        chart = TimeSeriesChart(
            self.df,
            columns=columns,
            target=self.target,
            date_column=self.date_column,
            model=self.config.time_series_config.model,
            period=self.config.time_series_config.period,
            output_dir=self.output_dir
        )
        self._append_chart("time_series_chart", chart.generate())
        return self

    def add_outliers_chart(self) -> Self:
        """
        Add an outliers chart to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        config = self.config.outlier_chart_layout_config
        chart = OutlierChart(
            df=self.df,
            columns=config.columns,
            max_cols_per_chart=config.max_cols_per_chart,
            single_image=config.single_image,
            output_dir=self.output_dir
        )
        self._append_chart("outliers_chart", chart.generate())
        return self

    # ================================
    # CHART SECTIONS - Analysis Charts
    # ================================

    def add_vif_chart(self) -> Self:
        """
        Add a VIF chart to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        config = self.config.vif_config
        chart = VIFChart(
            df=self.df,
            target_column=config.target_column,
            features=config.features,
            precision=config.precision,
            color_thresholds=config.color_thresholds,
            output_dir=self.output_dir
        )
        self._append_chart("vif_chart", chart.generate())
        return self

    def add_time_comparison_chart(self) -> Self:
        """
        Add a time comparison chart to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        config = self.config.time_comparison_chart_config
        report = TimeComparisonReport(
            df=self.df,
            date_column=config.date_column,
            value_columns=config.value_columns,
            comparison_type=config.comparison_type,
            agg_func=config.agg_func
        )

        chart = ComparisonChart(
            data=report.generate(),
            comparison_type=config.comparison_type,
            mode=config.mode,
            output_dir=self.output_dir
        )
        self._append_chart("comparison_chart", chart.generate())
        return self

    def add_lag_correlation_chart(self) -> Self:
        """
        Add a lag correlation chart to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        config = self.config.lag_corr_chart_config
        chart = LagCorrelationChart(
            df=self.df,
            column=config.column,
            lag=config.lag,
            output_dir=self.output_dir
        )
        self._append_chart("lag_correlation_chart", chart.generate())
        return self

    # ===================================
    # CHART SECTIONS - Data-Driven Charts
    # ===================================

    def add_acf_pacf_chart(self) -> Self:
        """
        Add an ACF/PACF chart to the report, if data is available.

        Returns:
            Self: The current instance for method chaining.
        """
        data = self._chart_data_cache.get("acf_pacf")
        if data is None:
            return self

        chart = ACFPACFPlotter(data=data, output_dir=self.output_dir)
        path = chart.generate()

        if path is not None:
            self._append_chart("acf_pacf_chart", path)
        return self

    def add_kpi_vs_feature_chart(self) -> Self:
        """
        Add a KPI vs. feature chart to the report, if data is available.

        Returns:
            Self: The current instance for method chaining.
        """
        data = self._chart_data_cache.get("dual_axis")
        if data is None:
            return self

        chart = DualAxisLinePlotter(data=data, output_dir=self.output_dir)
        path = chart.generate()

        if path is not None:
            self._append_chart("kpi_vs_feature_chart", path)
        return self

    def add_categorical_distribution_chart(self) -> Self:
        """
        Add a categorical distribution chart to the report, if data is available.

        Returns:
            Self: The current instance for method chaining.
        """
        if not self.config.categorical_columns_config.columns:
            print("No categorical columns specified. Skipping categorical distribution chart.\n"
                  "Use update_categorical_columns_config(columns=...) method to update the "
                  "categorical columns in the config first.")
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

    def add_report_title(self, title: str = "OwlMix EDA Report") -> Self:
        """
        Add a report title section.

        Args:
            title (str, optional): The report title. Defaults to "OwlMix EDA Report".

        Returns:
            Self: The current instance for method chaining.
        """
        self._add_section("title", title)
        return self

    def add_header_title(self, title: str = "🦉 OwlMix EDA Report") -> Self:
        """
        Add a header title section.

        Args:
            title (str, optional): The header title. Defaults to "🦉 OwlMix EDA Report".

        Returns:
            Self: The current instance for method chaining.
        """
        self._add_section("header_title", title)
        return self

    def add_header_subtitle(self, subtitle: Optional[str] = None) -> Self:
        """
        Add a header subtitle section.

        Args:
            subtitle (Optional[str], optional): The header subtitle. Defaults to a preset string.

        Returns:
            Self: The current instance for method chaining.
        """
        subtitle = subtitle or "Exploratory Data Analysis for Marketing Mix Modeling"
        self._add_section("header_subtitle", subtitle)
        return self

    def add_columns_as_list(self) -> Self:
        """
        Add a section listing all dataframe columns.

        Returns:
            Self: The current instance for method chaining.
        """
        self._add_section("columns", self.df.columns.tolist())
        return self

    def add_footer(self, text: str = "Generated by OwlMix EDA") -> Self:
        """
        Add a footer section with generator info and report date.

        Args:
            text (str, optional): Footer text. Defaults to "Generated by OwlMix EDA".

        Returns:
            Self: The current instance for method chaining.
        """
        self._add_section("generator", text)
        self._add_section("report_date", pd.Timestamp.now().isoformat())
        return self

    # =========================
    # BUILD ALL SECTIONS
    # =========================

    def add_all_non_charts(self) -> Self:
        """
        Add all non-chart sections to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        for _, func in self._non_charts.items():
            func()
        return self

    def add_all_charts(self) -> Self:
        """
        Add all chart sections to the report, respecting include/exclude and custom order.

        Returns:
            Self: The current instance for method chaining.
        """
        charts_to_run = self._resolve_charts()
        for chart in charts_to_run:
            self._charts[chart]()
        return self

    def add_all(self) -> Self:
        """
        Add all sections (non-charts and charts) to the report.

        Returns:
            Self: The current instance for method chaining.
        """
        self.add_all_non_charts()
        self.add_all_charts()
        return self

    # =========================
    # OUTPUT METHODS
    # =========================

    def build(self) -> dict:
        """
        Build the final report dictionary.

        Returns:
            dict: The report as a dictionary with 'sections' and 'charts'.
        """
        return {
            "sections": self.sections,
            "charts": self.chart_paths
        }

    def save(self, filename: str = "eda_report.json") -> None:
        """
        Save the report to a JSON file.

        Args:
            filename (str, optional): The filename for the report. Defaults to "eda_report.json".
        """
        result = self.build()
        if os.path.dirname(filename):
            file_path = filename
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        else:
            file_path = os.path.join(self.output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

    def _image_to_base64(self, image_path: str) -> str:
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

        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

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
