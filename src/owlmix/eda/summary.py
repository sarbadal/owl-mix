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
 
 
class SummaryBuilder:
    def __init__(self, df: pd.DataFrame, target: str | None, date_column: str, output_dir: str = "eda_output"):
        self.df = df
        self.target = target
        self.date_column = date_column
        self.output_dir = output_dir
 
        self.sections = []
        self.chart_paths = []

        self.outlier_chart_config = {
            "columns": None,
            "max_cols_per_chart": 4,
            "single_image": True
        }

        self.correlation_chart_config = {
            "columns": None,
            "precision": 2
        }

        self.correlation_config = {
            "columns": None
        }

        self.time_comparison_config = {
            "value_columns": None,
            "comparison_type": "yoy",
            "agg_func": "sum",
            "precision": 2
        }

        self.vif_config = {
            "target_column": self.target,
            "features": None,
            "precision": 3
        }

        self.acf_pacf_config = {
            "columns": None,
            "n_lags": 15
        }

        self.categorical_columns = {
            "columns": None
        }

        self.kpi_vs_feature_config = {
            "target_column": self.target,
            "columns": None,
            "date_format": "%Y-%m-%d",
            "date_column": self.date_column,
            "agg_func": "sum",
        }
 
        os.makedirs(self.output_dir, exist_ok=True)

    def set_vif_config(self, target_column: str = None, features: list[str] = None, precision: int = 3) -> Self:
        if not isinstance(precision, int) or precision < 1:
            raise ValueError("precision must be a positive integer")

        self.vif_config["target_column"] = target_column
        self.vif_config["features"] = features
        self.vif_config["precision"] = precision

        return self

    def set_kpi_vs_feature_config(self, target_column: str = None, columns: list[str] = None, date_column: str = None, date_format: str = "%Y-%m-%d", agg_func: str = "sum") -> Self:
        self.kpi_vs_feature_config["target_column"] = target_column or self.target
        self.kpi_vs_feature_config["date_format"] = date_format
        self.kpi_vs_feature_config["date_column"] = date_column or self.date_column
        self.kpi_vs_feature_config["agg_func"] = agg_func
        self.kpi_vs_feature_config["columns"] = columns

        return self

    def set_acf_pacf_config(self, columns: list[str] = None, n_lags: int = 15) -> Self:
        self.acf_pacf_config["columns"] = columns
        self.acf_pacf_config["n_lags"] = n_lags

        return self

    def set_correlation_config(self, columns: list[str] = None) -> Self:
        self.correlation_config["columns"] = columns

        return self

    def set_time_comparison_config(self, date_column: str = None, value_columns: list[str] = None, comparison_type: str = "yoy", agg_func: str = "sum", precision: int = 2) -> Self:
        if not isinstance(precision, int) or precision < 1:
            raise ValueError("precision must be a positive integer")

        self.time_comparison_config["date_column"] = date_column if date_column else self.date_column
        self.time_comparison_config["value_columns"] = value_columns
        self.time_comparison_config["comparison_type"] = comparison_type
        self.time_comparison_config["agg_func"] = agg_func
        self.time_comparison_config["precision"] = precision

        return self

    def set_outlier_chart_layout(self, columns: list[str]=None, max_cols_per_chart: int=4, single_image: bool=True) -> Self:
        if not isinstance(max_cols_per_chart, int) or max_cols_per_chart < 1:
            raise ValueError("max_cols_per_chart must be a positive integer")

        self.outlier_chart_config["max_cols_per_chart"] = max_cols_per_chart
        self.outlier_chart_config["single_image"] = single_image
        self.outlier_chart_config["columns"] = columns

        return self

    def set_correlation_chart_layout(self, columns: list[str]=None, precision: int=2):
        if not isinstance(precision, int) or precision < 1:
            raise ValueError("precision must be a positive integer")

        self.correlation_chart_config["columns"] = columns
        self.correlation_chart_config["precision"] = precision

        return self

    def set_categorical_columns(self, columns: list[str] = None) -> Self:
        self.categorical_columns["columns"] = columns

        return self
 
    # =========================
    # TEXT SECTIONS
    # =========================
 
    def add_basic_info(self):
        basic = BasicInfo(self.df)
        json_content = basic.to_json()
        self.sections.append({"basic_info": json.loads(json_content)})
        return self

    def add_vif_calculator(self, target_column: str = None, features: list[str] = None, precision: int = 3) -> Self:
        target_column = target_column or self.vif_config["target_column"]
        features = features or self.vif_config["features"]
        precision = self.vif_config["precision"]

        vif_calculator = VIFCalculator(
            df=self.df,
            target_column=target_column,
            features=features,
            precision=precision
        )
        self.sections.append({"vif": vif_calculator.compute_vif()})

        return self

    def add_kpi_vs_feature(self, target_column: str = None, features: list[str] = None) -> Self:
        target_column = target_column or self.kpi_vs_feature_config["target_column"]
        date_format = self.kpi_vs_feature_config["date_format"]
        date_column = self.kpi_vs_feature_config["date_column"]
        agg_func = self.kpi_vs_feature_config["agg_func"]
        columns = self.kpi_vs_feature_config["columns"]

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

    def add_causality_test(self, target_column: str = None, columns: list[str] = None, max_lag: int = 5, error_threshold: float = 0.30) -> Self:
        target_column = target_column or self.target

        causality_test = CausalityTest(
            df=self.df,
            target_column=target_column,
            columns=columns
        )

        result = causality_test.run(max_lag=max_lag, error_threshold=error_threshold)
        self.sections.append({"causality_test": result})

        return self

    def add_correlation_matrix(self, columns: list[str] = None) -> Self:
        columns = columns or self.correlation_config["columns"]
        corr = Correlation(df=self.df, columns=columns)
        self.sections.append({"correlation_matrix": corr.compute_correlation_matrix()})
        self.sections.append(
            {
                "lag_correlation": corr.compute_lag_correlation(
                    self.target, 
                    self.target, 
                    lags=[1, 2, 3]
                )
            }
        )
        return self

    def add_time_comparison(self, date_column: str = None, value_columns: list[str] = None, comparison_type: str = "yoy", agg_func: str = "sum") -> Self:
        date_column = date_column or self.time_comparison_config["date_column"]
        value_columns = value_columns or self.time_comparison_config["value_columns"]
        comparison_type = comparison_type or self.time_comparison_config["comparison_type"]
        agg_func = agg_func or self.time_comparison_config["agg_func"]
        precision = self.time_comparison_config["precision"]

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

    def add_time_aggregator(self, date_column: str=None, value_columns: list[str]=None, freq: str="YE", agg_func: str="sum") -> Self:
        date_column = date_column or self.date_column
        report = TimeAggregatorReport(
            df=self.df,
            date_column=date_column,
            value_columns=value_columns,
            freq=freq,
            agg_func=agg_func
        )
        result = report.aggregate()
        self.sections.append({"time_aggregator": result})

        return self

    def add_categorical_distribution(self, columns: list[str] = None) -> Self:
        columns = columns or self.categorical_columns["columns"]
        generator = CategoricalDistributionGenerator(
            df=self.df,
            columns=columns
        )
        result = generator.generate()

        self.sections.append({"categorical_distribution": result})
        self._categorical_chart_data = result["data"]

        return self

    def add_acf_pacf_calculator(self, columns: list[str]=None, n_lags: int = None) -> Self:
        columns = columns or self.acf_pacf_config["columns"]
        n_lags = n_lags or self.acf_pacf_config["n_lags"]
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

    def add_vif_chart(self, target_column: str = None, features: list[str] = None, precision: int = 3) -> Self:
        target_column = target_column or self.vif_config["target_column"]
        features = features or self.vif_config["features"]
        precision = self.vif_config["precision"]

        description = (
            "The Variance Inflation Factor (VIF) chart visualizes the degree of multicollinearity "
            "among the feature variables by displaying their respective VIF values. Higher VIF values "
            "indicate stronger linear relationships with other predictors, which may lead to instability "
            "in model coefficients and reduced interpretability. This chart enables quick identification "
            "of problematic variables by highlighting those exceeding commonly accepted thresholds, "
            "helping guide feature selection and dimensionality reduction decisions."
        )

        chart = VIFChart(
            df=self.df,
            target_column=target_column,
            features=features,
            precision=precision,
            output_dir=self.output_dir
        )
        path = chart.generate()
        self.chart_paths.append(
            {
                "title": "VIF Chart",
                "description": description,
                "vif_chart": path,
                "image_data": self._image_to_base64(path),
                "alt_text": "VIF Chart"
            }
        )
        return self

    def add_acf_pacf_chart(self) -> Self:
        description = (
            "The ACF (Autocorrelation Function) and PACF (Partial Autocorrelation Function) plots "
            "illustrate the correlation of each variable with its past values across different lag intervals. "
            "These charts help identify temporal dependencies, seasonality, and potential lag effects within "
            "the data. The inclusion of a smoothed trend line provides a clearer view of how correlations "
            "decay or persist as the lag increases, aiding in the detection of significant lag structures. "
            "This visualization is particularly useful for determining appropriate lag selections and "
            "understanding the underlying time-series behavior of the variables."
        )

        chart = ACFPACFPlotter(
            data=self._acf_pacf_chart_data,
            output_dir=self.output_dir
        )
        path = chart.generate()
        if path is None:
            return self

        self.chart_paths.append(
            {
                "title": "ACF PACF Chart",
                "description": description,
                "acf_pacf_chart": path,
                "image_data": self._image_to_base64(path),
                "alt_text": "ACF PACF Chart"
            }
        )
        return self

    def add_kpi_vs_feature_chart(self) -> Self:
        chart = DualAxisLinePlotter(
            data=self._dual_axis_chart_data,
            output_dir=self.output_dir
        )
        path = chart.generate()
        if path is None:
            return self

        description = (
            "This chart compares the target (KPI) variable with an individual feature variable over time using dual axes. "
            "By plotting both series together, it helps visually assess co-movement, trends, and potential "
            "relationships between the KPI and each feature across different periods."
        )

        self.chart_paths.append(
            {
                "title": "KPI VS Feature Chart",
                "description": description,
                "kpi_vs_feature_chart": path,
                "image_data": self._image_to_base64(path),
                "alt_text": "KPI VS Feature Chart"
            }
        )
        return self

    def add_distribution_chart(self, columns: list[str] = None) -> Self:
        description = (
            "The distribution chart illustrates the frequency distribution of the selected "
            "numerical variable across defined bins, providing a clear view of its spread and concentration. "
            "The overlaid normal distribution curve serves as a reference to assess how closely the data follows "
            "a Gaussian pattern, helping identify skewness, kurtosis, or deviations from normality. "
            "This visualization is useful for detecting outliers, understanding variability, and evaluating whether "
            "statistical assumptions (e.g., normality) are appropriate for subsequent modeling."
        )

        columns = columns or self.correlation_config["columns"]

        chart = DistributionChart(
            df=self.df,
            columns=columns,
            output_dir=self.output_dir
        )
        path = chart.generate()
        self.chart_paths.append(
            {
                "title": "Distribution Chart",
                "description": description,
                "distribution_chart": path,
                "image_data": self._image_to_base64(path),
                "alt_text": "Distribution Chart"
            }
        )
        return self

    def add_categorical_distribution_chart(self) -> Self:
        description = (
            "The categorical distribution chart presents the frequency of each category, allowing "
            "for a clear comparison of how observations are distributed across different groups. "
            "The categories are ordered by their counts to form a bell-shaped pattern, making "
            "it easier to visually identify the most and least dominant categories. This arrangement "
            "highlights concentration, imbalance, or sparsity within the data, helping uncover dominant "
            "segments and potential data skew that may influence downstream analysis or modeling decisions."
        )
        if not self.categorical_columns["columns"]:
            return self

        chart = CategoricalDistributionChart(
            data=self._categorical_chart_data,
            output_dir=self.output_dir
        )
        path = chart.generate()
        self.chart_paths.append(
            {
                "title": "Categorical Distribution Chart",
                "description": description,
                "categorical_distribution_chart": path,
                "image_data": self._image_to_base64(path),
                "alt_text": "Categorical Distribution Chart"
            }
        )
        return self

    def add_correlation_chart(self, columns: list[str]=None, precision: int=None):
        if columns is None:
            columns = self.correlation_chart_config["columns"]

        if precision is None:
            precision = self.correlation_chart_config["precision"]

        description = (
            "The correlation heatmap visualizes pairwise relationships between variables using color "
            "intensity to represent the strength and direction of correlations. This chart enables quick "
            "identification of highly correlated variable pairs, patterns, and potential multicollinearity within the dataset."
        )

        chart = CorrelationChart(
            df=self.df,
            columns=columns,
            precision=precision,
            output_dir=self.output_dir
        )
        path = chart.generate()
        self.chart_paths.append(
            {
                "title": "Correlation Chart",
                "description": description,
                "correlation_chart": path,
                "image_data": self._image_to_base64(path),
                "alt_text": "Correlation Chart"
            }
        )
        return self
 
    def add_time_series_chart(self, columns=None):
        description = (
            "This chart presents the target (KPI) variable over time, along with its decomposition "
            "into trend, seasonality, and residual components. The observed series reflects the actual values, "
            "while the decomposed plots isolate underlying patterns, helping to understand long-term movement, "
            "recurring seasonal effects, and unexplained variations in the data."
        )
        chart = TimeSeriesChart(
            self.df, 
            columns=columns, 
            target=self.target,
            date_column=self.date_column,
            output_dir=self.output_dir
        )
        path = chart.generate()
        self.chart_paths.append(
            {
                "title": "Time Series Chart",
                "description": description,
                "time_series_chart": path,
                "image_data": self._image_to_base64(path),
                "alt_text": "Time Series Chart"
            }
        )
        return self
 
    def add_outliers_chart(self, columns=None, max_cols_per_chart: int=None, single_image: bool=None):
        if max_cols_per_chart is None:
            max_cols_per_chart = self.outlier_chart_config["max_cols_per_chart"]

        if single_image is None:
            single_image = self.outlier_chart_config["single_image"]

        if columns is None:
            columns = self.outlier_chart_config["columns"]

        chart = OutlierChart(
            df=self.df,
            columns=columns, 
            max_cols_per_chart=max_cols_per_chart,
            single_image=single_image,
            output_dir=self.output_dir
        )
        path = chart.generate()
        description = (
            "The box plot visualizes the distribution of the target and feature variables, highlighting "
            "their median, spread, and potential outliers. It enables quick identification of extreme values "
            "and variability across variables, supporting data quality assessment and informed preprocessing decisions."
        )

        self.chart_paths.append(
            {
                "title": "Outliers Chart",
                "description": description,
                "outliers_chart": path,
                "image_data": self._image_to_base64(path),
                "alt_text": "Outliers Chart"
            }
        )
        return self

    def add_comparison_chart(self, date_column: str=None, value_columns: list[str]=None, freq="ME", comparison="yoy") -> Self:
        date_column = date_column or self.date_column
        # value_columns = value_columns or [self.target]

        description = (
            "The Year-over-Year (YoY) line chart visualizes the annual percentage change in key variables, "
            "enabling a clear comparison of growth or decline trends over time. Each line represents a "
            "distinct variable, highlighting how its performance evolves relative to the previous year. "
            "This chart helps identify consistent trends, seasonal patterns, and periods of significant "
            "change across multiple variables."
        )

        chart = ComparisonChart(
            df=self.df,
            date_column=date_column,
            value_columns=value_columns,
            freq=freq,
            comparison=comparison,
            output_dir=self.output_dir,
        )

        path = chart.generate()

        self.chart_paths.append(
            {
                "title": f"Comparison Chart - {comparison.upper()}",
                "description": description,
                "comparison_chart": path,
                "image_data": self._image_to_base64(path),
                "alt_text": f"Comparison Chart - {comparison.upper()}"
            }
        )

        return self
 
    def add_lag_correlation(self, lag=1):
        chart = LagCorrelationChart(
            df=self.df, 
            column=self.target, 
            output_dir=self.output_dir, 
            lag=lag)
        path = chart.generate()
        description = (
            "This scatter plot illustrates the relationship between the target (KPI) variable and "
            "its lagged value (lag 1), comparing current values (T) against the previous period (T−1). "
            "It helps visualize the strength and direction of short-term temporal dependency, indicating "
            "how strongly the current value is influenced by its immediate past."
        )

        self.chart_paths.append(
            {
                "title": "Lag Correlation Chart",
                "description": description,
                "lag_correlation_chart": path,
                "image_data": self._image_to_base64(path),
                "alt_text": "Lag Correlation Chart"
            }
        )
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
            .add_lag_correlation()
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
