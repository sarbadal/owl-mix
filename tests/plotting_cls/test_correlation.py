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
from owlmix.plotting.correlation import CorrelationPlotter, CorrPlotParams

def test_correlation_plotter():
    # Generate sample data
    df = create_sample_data(n=100)

    # Define parameters for CorrelationAnalyzer
    params = CorrelationParams(
        columns=None,  # Use all numeric columns
        n_lags=25,
        precision=4
    )

    # Create and compute the analyzer
    analyzer = CorrelationAnalyzer(df, params)
    result = analyzer.compute()
    # analyzer.print_results(result)
    # print(result["lagged_correlation_matrix"])

    # Create and generate the plotter
    plotter = CorrelationPlotter(result)
    corr_file_path, lagged_corr_file_path = plotter.generate()
    print(f"Correlation matrix saved to: {corr_file_path}")
    print(f"Lagged correlation matrix saved to: {lagged_corr_file_path}")

if __name__ == "__main__":    
    test_correlation_plotter()