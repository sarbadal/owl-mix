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
from owlmix.utils.sample_data_generator import create_sample_data
from owlmix.plotting.time_series import TimeSeriesPlotter, TimeSeriesPlotParams

def test_time_series_analysis():
    df = create_sample_data(n=300)
    params = TimeSeriesPlotParams(
        date_column="time",
        target_column="sales",
        period=None,
        model="additive"
    )
    plotter = TimeSeriesPlotter(df=df, params=params)
    charts = plotter.plot()
    # print(charts)

if __name__ == "__main__":
    test_time_series_analysis()