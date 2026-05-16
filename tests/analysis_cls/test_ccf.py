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
from owlmix.analysis.cross_correlation_func_ccf import CCFAnalyzer, CCFParams


def test_ccf_analyzer():
    df = create_sample_data(n=100)
    params = CCFParams(
        time_column="time",
        target_column="sales",
        feature_columns=['tv_spend', 'digital_spend'],
        max_lag=3
    )
    analyzer = CCFAnalyzer(df, params)
    result = analyzer.compute()
    # analyzer.print_results_json(result)
    analyzer.print_results()


if __name__ == "__main__":
    test_ccf_analyzer()