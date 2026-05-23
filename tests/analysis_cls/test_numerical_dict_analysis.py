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
from owlmix.analysis.dist_numerical import NumericalDistributionAnalysis, NumericalDistributionParams
from owlmix.plotting.dist_numerical import NumericalDistributionPlotter

def test_numerical_distribution_analysis():
    # Generate sample data
    df = create_sample_data(n=3000)

    # Define parameters for NumericalDistributionAnalysis
    params = NumericalDistributionParams(
        # columns=["sales", "tv_spend"],
        precision=2,
        bins=150
    )

    # Create and compute the analysis
    analysis = NumericalDistributionAnalysis(df, params)
    results = analysis.compute()
    # analysis.print_results(results)

    plotter = NumericalDistributionPlotter(results)
    files = plotter.generate("output/charts")

if __name__ == "__main__":    
    test_numerical_distribution_analysis()