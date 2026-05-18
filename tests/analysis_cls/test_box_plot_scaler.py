import os, sys
import warnings
from pathlib import Path

warnings.simplefilter('ignore', category=UserWarning)

# Add src to the path
CURRENT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = CURRENT_DIR / "src"
sys.path.append(str(SRC_DIR))
#===============================================================================
import pandas as pd
from owlmix.analysis.box_plot import BoxPlotData, PlotConfig, BoxPlotScalerConfig, build_box_plot_scaler_config
from owlmix.analysis.box_plot import BoxPlotScaler

json_data = {
    "column": "tv_spend",
    "min": 100.0,
    "Q1": 200.25,
    "median": 306.0,
    "mean": 289,
    "Q3": 402.0,
    "max": 499.0,
    "outliers_count": 12,
    "outliers": [
        496.0,
        101.0,
        107.0
    ]
}

def test_box_plot_scaler():
    box_plot_scaler_config = build_box_plot_scaler_config(
        data=json_data,
    )
    scaler = BoxPlotScaler(config=box_plot_scaler_config)
    scaler_data = scaler.build()
    scaler.print_results_json(scaler_data)
    scaler.print_results(scaler_data, include_outliers=True)
    # print(scaler_data)

if __name__ == "__main__":
    test_box_plot_scaler()