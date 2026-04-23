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
 
        os.makedirs(self.output_dir, exist_ok=True)

    # =========================
    # TEXT SECTIONS
    # =========================
 
    def add_basic_info(self):
        basic = BasicInfo(self.df)
        json_content = basic.to_json()
        self.sections.append({"basic_info": json.loads(json_content)})
        return self

    def add_vif_calculator(self, target_column: str = None, features: list[str] = None, precision: int = 3) -> Self:
        target_column = target_column or self.config.vif_config["target_column"]
        features = features or self.config.vif_config["features"]
        precision = self.config.vif_config["precision"]

        vif_calculator = VIFCalculator(
            df=self.df,
            target_column=target_column,
            features=features,
            precision=precision
        )
        self.sections.append({"vif": vif_calculator.compute_vif()})

        return self

    def add_kpi_vs_feature(self, target_column: str = None, features: list[str] = None) -> Self:
        target_column = target_column or self.config.kpi_vs_feature_config["target_column"]
        date_format = self.config.kpi_vs_feature_config["date_format"]
        date_column = self.config.kpi_vs_feature_config["date_column"]
        agg_func = self.config.kpi_vs_feature_config["agg_func"]
        columns = self.config.kpi_vs_feature_config["columns"]

        kpi_vs_feature_generator = DualAxisLineChartDataGenerator(
            df=self.df,
            target_column=target_column,
            columns=columns,
            date_format=date_format,
            date_column=date_column,
            agg_func=agg_func,
        )
        result = kpi_vs_feature_generator.generate()
        self.sections.append({"kpi_vs_features": result})
        self._dual_axis_chart_data = result["data"]

        return self

    def add_causality_test(self) -> Self:
        target_column = self.config.causality_test_config["target_column"]
        columns = self.config.causality_test_config["columns"]
        max_lag = self.config.causality_test_config["max_lag"]
        error_threshold = self.config.causality_test_config["error_threshold"]

        causality_test = CausalityTest(
            df=self.df,
            target_column=target_column,
            columns=columns
        )

        result = causality_test.run(max_lag=max_lag, error_threshold=error_threshold)
        self.sections.append({"causality_test": result})

        return self

    def add_correlation_matrix(self) -> Self:
        columns = self.config.correlation_config["columns"]
        corr = Correlation(
            df=self.df,
            columns=columns
        )

        self.sections.append({"correlation_matrix": corr.compute_correlation_matrix()})
        self.sections.append(
            {
                "lag_correlation": corr.compute_lag_correlation(
                    self.target, 
                    self.target, 
                    lags=[1, 2, 3, 4, 5]
                )
            }
        )
        return self

    def add_time_comparison(self) -> Self:
        date_column = self.config.time_comparison_config["date_column"]
        value_columns = self.config.time_comparison_config["value_columns"]
        comparison_type = self.config.time_comparison_config["comparison_type"]
        agg_func = self.config.time_comparison_config["agg_func"]
        precision = self.config.time_comparison_config["precision"]

        report = TimeComparisonReport(
            df=self.df,
            date_column=date_column,
            value_columns=value_columns,
            comparison_type=comparison_type,
            agg_func=agg_func,
            precision=precision
        )

        result = report.generate()
        self.sections.append({"time_comparison": result})

        return self

    def add_time_aggregator(self) -> Self:
        date_column = self.config.time_aggregator_config["date_column"]
        value_columns = self.config.time_aggregator_config["value_columns"]
        freq = self.config.time_aggregator_config["freq"]
        agg_func = self.config.time_aggregator_config["agg_func"]
        precision = self.config.time_aggregator_config["precision"]


        report = TimeAggregatorReport(
            df=self.df,
            date_column=date_column,
            value_columns=value_columns,
            freq=freq,
            agg_func=agg_func,
            precision=precision
        )
        result = report.aggregate()
        self.sections.append({"time_aggregator": result})

        return self

    def add_categorical_distribution(self, columns: list[str] = None) -> Self:
        columns = columns or self.config.categorical_columns_config["columns"]
        generator = CategoricalDistributionGenerator(
            df=self.df,
            columns=columns
        )
        result = generator.generate()

        self.sections.append({"categorical_distribution": result})
        self._categorical_chart_data = result["data"]

        return self

    def add_acf_pacf_calculator(self, columns: list[str]=None, n_lags: int = None) -> Self:
        columns = columns or self.config.acf_pacf_config["columns"]
        n_lags = n_lags or self.config.acf_pacf_config["n_lags"]
        generator = ACFPACFCalculator(
            df=self.df,
            columns=columns,
            n_lags=n_lags
        )
        result = generator.generate()

        self.sections.append({"acf_pacf": result})
        self._acf_pacf_chart_data = result["data"]

        return self
 
    # =========================
    # CHART SECTIONS
    # =========================

    def _append_chart(self, chart_id: str, path: str) -> None:
        """Helper method to append a chart to a chart path."""
        title = self.title_config.charts[chart_id].title
        description = self.title_config.charts[chart_id].description
        alt_text = self.title_config.charts[chart_id].alt_text

        self.chart_paths.append(
            {
                "title": title,
                "description": description,
                chart_id: path,
                "image_data": self._image_to_base64(path),
                "alt_text": alt_text
            }
        )

    def add_vif_chart(self) -> Self:
        target_column = self.config.vif_config["target_column"]
        features = self.config.vif_config["features"]
        precision = self.config.vif_config["precision"]

        chart = VIFChart(
            df=self.df,
            target_column=target_column,
            features=features,
            precision=precision,
            output_dir=self.output_dir
        )
        path = chart.generate()

        self._append_chart(chart_id="vif_chart", path=path)

        return self

    def add_acf_pacf_chart(self) -> Self:
        chart = ACFPACFPlotter(
            data=self._acf_pacf_chart_data,
            output_dir=self.output_dir
        )
        path = chart.generate()

        if path is None:
            return self

        self._append_chart(chart_id="acf_pacf_chart",path=path)

        return self

    def add_kpi_vs_feature_chart(self) -> Self:
        chart = DualAxisLinePlotter(
            data=self._dual_axis_chart_data,
            output_dir=self.output_dir
        )
        path = chart.generate()
        if path is None:
            return self

        self._append_chart(chart_id="kpi_vs_feature_chart", path=path)

        return self

    def add_distribution_chart(self) -> Self:
        columns = self.config.correlation_config["columns"]

        chart = DistributionChart(
            df=self.df,
            columns=columns,
            output_dir=self.output_dir
        )
        path = chart.generate()

        self._append_chart(chart_id="distribution_chart", path=path)

        return self

    def add_categorical_distribution_chart(self) -> Self:
        if not self.config.categorical_columns_config["columns"]:
            return self

        chart = CategoricalDistributionChart(
            data=self._categorical_chart_data,
            output_dir=self.output_dir
        )
        path = chart.generate()

        self._append_chart(chart_id="categorical_distribution_chart", path=path)

        return self

    def add_correlation_chart(self):
        columns = self.config.correlation_chart_layout_config["columns"]
        precision = self.config.correlation_chart_layout_config["precision"]

        chart = CorrelationChart(
            df=self.df,
            columns=columns,
            precision=precision,
            output_dir=self.output_dir
        )
        path = chart.generate()

        self._append_chart(chart_id="correlation_chart", path=path)

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
        path = chart.generate()

        self._append_chart(chart_id="time_series_chart", path=path)

        return self
 
    def add_outliers_chart(self):
        max_cols_per_chart = self.config.outlier_chart_layout_config["max_cols_per_chart"]
        single_image = self.config.outlier_chart_layout_config["single_image"]
        columns = self.config.outlier_chart_layout_config["columns"]

        chart = OutlierChart(
            df=self.df,
            columns=columns, 
            max_cols_per_chart=max_cols_per_chart,
            single_image=single_image,
            output_dir=self.output_dir
        )
        path = chart.generate()

        self._append_chart(chart_id="outliers_chart", path=path)

        return self

    def add_comparison_chart(self) -> Self:
        date_column = self.config.time_comparison_config["date_column"]
        value_columns = self.config.time_comparison_config["value_columns"]
        freq = self.config.time_comparison_config["freq"]
        comparison = self.config.time_comparison_config["comparison"]
        agg_func = self.config.time_comparison_config["agg_func"]

        chart = ComparisonChart(
            df=self.df,
            date_column=date_column,
            value_columns=value_columns,
            freq=freq,
            comparison=comparison,
            output_dir=self.output_dir,
        )

        path = chart.generate()

        self._append_chart(chart_id="comparison_chart", path=path)

        return self
 
    def add_lag_correlation_chart(self, lag=1):
        chart = LagCorrelationChart(
            df=self.df, 
            column=self.target, 
            output_dir=self.output_dir, 
            lag=lag)
        path = chart.generate()

        self._append_chart(chart_id="lag_correlation_chart", path=path)

        return self

    def add_report_title(self, title: str = "OwlMix EDA Report"):
        self.sections.append({"title": title})
        return self

    def add_header_title(self, title: str = "🦉 OwlMix EDA Report"):
        self.sections.append({"header_title": title})
        return self

    def add_header_subtitle(self, subtitle: str = None):
        subtitle = subtitle or "Exploratory Data Analysis for Marketing Mix Modeling"
        self.sections.append({"header_subtitle": subtitle})
        return self

    def add_columns_as_list(self):
        self.sections.append({"columns": self.df.columns.tolist()})
        return self

    def add_footer(self, text: str = "Generated by OwlMix EDA"):
        self.sections.append(
            {
                "generator": text,
                "report_date": pd.Timestamp.now().isoformat()
            }
        )
        return self

    # =========================
    # OPTIONAL: ADD EVERYTHING
    # =========================
 
    def add_all(self):
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
    # BUILD OUTPUT
    # =========================
 
    def build(self) -> dict:
        report = {
            "sections": self.sections,
            "charts": self.chart_paths
        }
        return report

    def save(self, filename: str = "eda_report.json"):
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
            if ext == '.png':
                mime_type = 'image/png'
            elif ext == '.jpg' or ext == '.jpeg':
                mime_type = 'image/jpeg'
            elif ext == '.gif':
                mime_type = 'image/gif'
            elif ext == '.webp':
                mime_type = 'image/webp'
            else:
                mime_type = 'image/png'  # default

            return f'data:{mime_type};base64,{encoded_string}'
