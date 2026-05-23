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
from owlmix.plotting.dist_numerical import NumericalDistributionPlotter, NumericalDistributionPlotParams


def test_numerical_distribution_analysis():
    df = create_sample_data(n=1000)
    params = NumericalDistributionPlotParams()
    plotter = NumericalDistributionPlotter(df=df, params=params)
    charts = plotter.plot()
    print(charts)


if __name__ == "__main__":
    test_numerical_distribution_analysis()