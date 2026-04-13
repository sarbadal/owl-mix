# src/owlmix/eda/summary.py

import os
import pandas as pd
import json

from owlmix.eda.basic import get_basic_info
from owlmix.eda.correlation import get_correlation_matrix, get_lag_correlation

from owlmix.eda.basic import BasicInfo
from owlmix.eda.stats import BasicStats
from owlmix.eda.correlation import Correlation
 
from owlmix.eda.charts.correlation import CorrelationChart
from owlmix.eda.charts.time_series import TimeSeriesChart
from owlmix.eda.charts.outliers import OutlierChart
from owlmix.eda.charts.lag import LagCorrelationChart
 
 
class SummaryBuilder:
    def __init__(self, df: pd.DataFrame, target: str | None, output_dir: str = "eda_output"):
        self.df = df
        self.target = target
        self.output_dir = output_dir
 
        self.sections = []
        self.chart_paths = []
 
        os.makedirs(self.output_dir, exist_ok=True)
 
    # =========================
    # TEXT SECTIONS
    # =========================
 
    def add_basic_info(self):
        basic = BasicInfo(self.df)
        json_content = basic.to_json()
        self.sections.append({"basic_info": json.loads(json_content)})
        return self

    def add_correlation_matrix(self):
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
 
    # =========================
    # CHART SECTIONS
    # =========================
 
    def add_correlation_chart(self):
        chart = CorrelationChart(self.df, self.output_dir)
        path = chart.generate()
        self.chart_paths.append({"correlation_chart": path})
        return self
 
    def add_time_series_chart(self, columns=None):
        chart = TimeSeriesChart(
            self.df, 
            columns=columns, 
            target=self.target,
            output_dir=self.output_dir
        )
        path = chart.generate()
        self.chart_paths.append({"time_series_chart": path})
        return self
 
    def add_outliers_chart(self, columns=None):
        chart = OutlierChart(self.df, columns=columns, output_dir=self.output_dir)
        path = chart.generate()
        self.chart_paths.append({"outliers_chart": path})
        return self
 
    def add_lag_correlation(self, lag=1):
        chart = LagCorrelationChart(
            df=self.df, 
            column=self.target, 
            output_dir=self.output_dir, 
            lag=lag)
        path = chart.generate()
        self.chart_paths.append({"lag_correlation_chart": path})
        return self
 
    # =========================
    # OPTIONAL: ADD EVERYTHING
    # =========================
 
    def add_all(self):
        return (
            self
            .add_basic_info()
            .add_correlation_matrix()
            .add_correlation_chart()
            .add_time_series_chart()
            .add_outliers_chart()
            .add_lag_correlation()
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
        print(f"Saving report to {filename}...")
        result = self.build()
        if os.path.dirname(filename):
            file_path = filename
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        else:
            file_path = os.path.join(self.output_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
