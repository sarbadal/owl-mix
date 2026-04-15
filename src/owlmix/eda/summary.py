# src/owlmix/eda/summary.py

import os
import base64
from typing import Self

import pandas as pd
import json

from owlmix.eda.basic import get_basic_info
from owlmix.eda.correlation import get_correlation_matrix, get_lag_correlation

from owlmix.eda.basic import BasicInfo
from owlmix.eda.stats import BasicStats
from owlmix.eda.correlation import Correlation
from owlmix.eda.time.comparison import TimeComparisonReport
from owlmix.eda.charts.time.comparison import ComparisonChart
 
from owlmix.eda.charts.correlation import CorrelationChart
from owlmix.eda.charts.time_series import TimeSeriesChart
from owlmix.eda.charts.outliers import OutlierChart
from owlmix.eda.charts.lag import LagCorrelationChart
 
 
class SummaryBuilder:
    def __init__(self, df: pd.DataFrame, target: str | None, date_column: srt, output_dir: str = "eda_output"):
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
 
        os.makedirs(self.output_dir, exist_ok=True)

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
 
    # =========================
    # TEXT SECTIONS
    # =========================
 
    def add_basic_info(self):
        basic = BasicInfo(self.df)
        json_content = basic.to_json()
        self.sections.append({"basic_info": json.loads(json_content)})
        return self

    def add_correlation_matrix(self) -> Self:
        corr = Correlation(self.df)
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

    def add_time_comparison(self, date_column: str=None, value_columns: list[str]=None, freq: str=None) -> Self:
        date_column = date_column or self.date_column
        # value_columns = value_columns or [self.target]
        # freq = freq or "ME"
        report = TimeComparisonReport(
            df=self.df,
            date_column=date_column,
            value_columns=value_columns,
            freq=freq
        )

        result = report.generate()
        self.sections.append({"time_comparison": result})

        return self
 
    # =========================
    # CHART SECTIONS
    # =========================
 
    def add_correlation_chart(self, columns: list[str]=None, precision: int=None):
        if columns is None:
            columns = self.correlation_chart_config["columns"]

        if precision is None:
            precision = self.correlation_chart_config["precision"]

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
                "description": "Correlation matrix plot",
                "correlation_chart": path,
                "image_data": self._image_to_base64(path),
                "alt_text": "Correlation Chart"
            }
        )
        return self
 
    def add_time_series_chart(self, columns=None):
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
                "description": "Time series plot for selected columns",
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
        self.chart_paths.append(
            {
                "title": "Outliers Chart",
                "description": "Outliers plot for selected columns",
                "outliers_chart": path,
                "image_data": self._image_to_base64(path),
                "alt_text": "Outliers Chart"
            }
        )
        return self

    def add_comparison_chart(self, date_column: str=None, value_columns: list[str]=None, freq="ME", comparison="yoy") -> Self:
        date_column = date_column or self.date_column
        # value_columns = value_columns or [self.target]

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
                "description": f"Comparison {comparison.upper()} plot for selected columns",
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
        self.chart_paths.append(
            {
                "title": "Lag Correlation Chart",
                "description": f"Lag correlation plot for {self.target}",
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
            .add_time_comparison()
            .add_time_series_chart()
            .add_outliers_chart()
            .add_lag_correlation()
            .add_comparison_chart()
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
