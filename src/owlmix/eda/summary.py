# src/owlmix/eda/summary.py

import os
import pandas as pd
 
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
        info = f"""
        <h2>Basic Information</h2>
        <ul>
            <li><b>Rows:</b> {self.df.shape[0]}</li>
            <li><b>Columns:</b> {self.df.shape[1]}</li>
        </ul>
        """
 
        self.sections.append(info)
        return self
 
    def add_missing_summary(self):
        missing = self.df.isnull().sum()
 
        html = "<h2>Missing Values</h2><ul>"
        for col, val in missing.items():
            html += f"<li>{col}: {val}</li>"
        html += "</ul>"
 
        self.sections.append(html)
        return self
 
    def add_descriptive_stats(self):
        desc = self.df.describe().to_html()
 
        html = f"""
        <h2>Descriptive Statistics</h2>
        {desc}
        """
 
        self.sections.append(html)
        return self
 
    # =========================
    # CHART SECTIONS
    # =========================
 
    def add_correlation_chart(self):
        chart = CorrelationChart(self.df, self.output_dir)
        path = chart.generate()
 
        self.chart_paths.append(path)
 
        self.sections.append(
            f"<h2>Correlation Matrix</h2><img src='{path}' width='600'/>"
        )
        return self
 
    def add_time_series_chart(self, columns=None):
        chart = TimeSeriesChart(
            self.df, 
            columns=columns, 
            target=self.target,
            output_dir=self.output_dir
        )
        path = chart.generate()
 
        self.chart_paths.append(path)
 
        self.sections.append(
            f"<h2>Time Series</h2><img src='{path}' width='600'/>"
        )
        return self
 
    def add_outliers_chart(self, columns=None):
        chart = OutlierChart(self.df, columns=columns, output_dir=self.output_dir)
        path = chart.generate()
 
        self.chart_paths.append(path)
 
        self.sections.append(
            f"<h2>Outliers (Box Plot)</h2><img src='{path}' width='600'/>"
        )
        return self
 
    def add_lag_correlation(self, lag=1):
        chart = LagCorrelationChart(
            df=self.df, 
            column=self.target, 
            output_dir=self.output_dir, 
            lag=lag)
        path = chart.generate()
 
        self.chart_paths.append(path)
 
        self.sections.append(
            f"<h2>Lag Correlation (lag={lag})</h2><img src='{path}' width='600'/>"
        )
        return self
 
    # =========================
    # OPTIONAL: ADD EVERYTHING
    # =========================
 
    def add_all(self):
        return (
            self
            .add_basic_info()
            .add_missing_summary()
            .add_descriptive_stats()
            .add_correlation_chart()
            .add_time_series_chart()
            .add_outliers_chart()
            .add_lag_correlation()
        )
 
    # =========================
    # BUILD OUTPUT
    # =========================
 
    def build(self) -> str:
        html = f"""
        <html>
        <head>
            <title>OwlMix EDA Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                h2 {{
                    color: #2c3e50;
                }}
                img {{
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    padding: 5px;
                }}
                table {{
                    border-collapse: collapse;
                }}
                table, th, td {{
                    border: 1px solid #ccc;
                    padding: 5px;
                }}
            </style>
        </head>
        <body>
        """
 
        html += "".join(self.sections)
 
        html += "</body></html>"
 
        return html
 
    def save(self, filename: str = "report.html"):
        if os.path.dirname(filename):
            file_path = filename
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        else:
            file_path = os.path.join(self.output_dir, filename)
 
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.build())
 
        return file_path