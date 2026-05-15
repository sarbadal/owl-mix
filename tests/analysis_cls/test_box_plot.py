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
from owlmix.analysis.box_plot import BoxPlotAnalyzer, BoxPlotParams

def test_box_plot_analyzer():
    df = create_sample_data(n=100)
    params = BoxPlotParams(
        # columns=["sales", "radio_spend", "digital_spend"],
        method="zscore",  # "iqr", "zscore"
        # threshold=1.5,
        precision=2
    )
    analyzer = BoxPlotAnalyzer(df, params)
    result = analyzer.compute()
    # print(result)

    # analyzer.print_results_json(result)
    analyzer.print_results(result, include_outliers=False)

if __name__ == "__main__":    
    test_box_plot_analyzer()