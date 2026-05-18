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
from owlmix.plotting.dual_axis_line import DualAxisLinePreparer, DualAxisLineDataConfig

def test_dual_axis_line_preparer():
    # Generate sample data
    df = create_sample_data(n=100)

    # Define parameters for DualAxisLinePreparer
    config = DualAxisLineDataConfig(
        time_column="time",
        target_column="sales",
        feature_column="tv_spend",
        normalize=True,
    )

    # Create and compute the preparer
    preparer = DualAxisLinePreparer(df, config)
    data = preparer.prepare()

    # Print the output for verification
    print("Dual Axis Line Output:", data)

if __name__ == "__main__":    
    test_dual_axis_line_preparer()