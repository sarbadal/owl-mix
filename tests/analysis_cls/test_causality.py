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
from owlmix.analysis.causality import CausalityAnalyzer, CausalityParams

def test_causality_analyzer():
    # Create sample data
    df = create_sample_data(n=15, seed=42, include_nan=False)
    print("Sample Data:")
    print(df.head(n=20), end="\n\n")

    # Define parameters for causality analysis
    params = CausalityParams(
        target_column="sales",
        columns=None,  # Use all numeric columns except target
        max_lag=5,
        precision=2,
        # error_threshold=0.2,
        p_value_weight=0.2,
        mape_weight=0.8
    )

    # Initialize and compute causality analysis
    analyzer = CausalityAnalyzer(df, params)
    results = analyzer.compute()

    # Print results in JSON format
    analyzer.print_results_json(results)

    # Print results in tabular format
    analyzer.print_results(results)

if __name__ == "__main__":
    test_causality_analyzer()