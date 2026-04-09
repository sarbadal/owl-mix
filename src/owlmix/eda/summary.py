# src/owlmix/eda/summary.py

import os
import pandas as pd
import textwrap

from .charts.correlation import CorrelationChart
from .charts.timeseries import TimeSeriesChart
from .charts.outliers import OutlierChart


class SummaryBuilder:
 
    def __init__(self, df, target=None, output_dir="outputs"):
        self.df = df
        self.target = target
        self.output_dir = output_dir
        self.sections = []
        self.chart_paths = []
 
    # -------------------------
    # TEXT SECTIONS
    # -------------------------
 
    def add_basic_info(self):
        info = []
        info.append("=== BASIC INFO ===")
        info.append(f"Shape: {self.df.shape}")
        info.append(f"Columns: {list(self.df.columns)}")
        info.append(f"Data Types:\n{self.df.dtypes}")
 
        self.sections.append("\n".join(map(str, info)))
        return self
 
    def add_missing_summary(self):
        missing = self.df.isna().sum()
        missing_pct = (missing / len(self.df)) * 100
 
        text = [
            "=== MISSING VALUES ===",
            str(missing),
            "Percentage:",
            str(missing_pct.round(2))
        ]
 
        self.sections.append("\n".join(text))
        return self
 
    def add_descriptive_stats(self):
        desc = self.df.describe(include="all").transpose()
 
        self.sections.append(
            "=== DESCRIPTIVE STATS ===\n" + str(desc)
        )
        return self
 
    # -------------------------
    # CHART SECTION
    # -------------------------
 
    def add_charts(self):
        chart_paths = []
 
        # Correlation
        corr_path = CorrelationChart(self.output_dir).plot(self.df)
        chart_paths.append(f"Correlation Heatmap: {corr_path}")
 
        # Time series (if applicable)
        if self.target:
            ts_path = TimeSeriesChart(self.output_dir).plot(
                self.df,
                value_cols=[self.target]
            )
            chart_paths.append(f"Time Series: {ts_path}")
 
        # Outliers
        out_path = OutlierChart(self.output_dir).plot(
            self.df,
            columns=self.df.select_dtypes(include="number").columns[:3]
        )
        chart_paths.append(f"Outliers: {out_path}")
 
        self.sections.append(
            "=== CHARTS ===\n" + "\n".join(chart_paths)
        )
 
        return self
 
    # -------------------------
    # FINAL BUILD
    # -------------------------
 
    def build(self):
        return "\n\n".join(self.sections)
 
    def save(self, filepath="outputs/eda_summary.txt"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        summary = self.build()
 
        with open(filepath, "w") as f:
            f.write(summary)
 
        return filepath