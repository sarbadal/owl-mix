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
from owlmix.analysis.correlation import CorrelationAnalyzer, CorrelationParams

def test_correlation_analyzer():
    # Generate sample data
    df = create_sample_data(n=100)

    # Define parameters for CorrelationAnalyzer
    params = CorrelationParams(
        # columns=None,  # Use all numeric columns
        # columns=["tv_spend", "radio_spend", "digital_spend"],  # Specify columns to analyze
        n_lags=5,
        precision=4
    )

    # Create and compute the analyzer
    analyzer = CorrelationAnalyzer(df, params)
    result = analyzer.compute()
    # print("Correlation Matrix:", result["correlation_matrix"])
    # print("Lagged Correlation Matrix:", result["lagged_correlation_matrix"])
    analyzer.print_results_json(result)
    analyzer.print_results(result)

if __name__ == "__main__":    
    test_correlation_analyzer()