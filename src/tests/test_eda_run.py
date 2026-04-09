# src/tests/test_eda_run.py

import sys
import os
 
# --------------------------------------------------
# Add src/ to path (so we can import owlmix locally)
# --------------------------------------------------
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
 
sys.path.insert(0, SRC_PATH)
 
# --------------------------------------------------
# Now we can import our package
# --------------------------------------------------
from owlmix.eda import OwlMixEDA
 
import pandas as pd
import numpy as np
 
 
def create_sample_data(n=100):
    """Create sample MMM-like dataset."""
    np.random.seed(42)
 
    dates = pd.date_range(start="2023-01-01", periods=n, freq="D")
 
    df = pd.DataFrame({
        "date": dates,
        "tv_spend": np.random.randint(100, 500, size=n),
        "digital_spend": np.random.randint(50, 300, size=n),
        "radio_spend": np.random.randint(20, 150, size=n),
    })
 
    # Create synthetic sales with some relationship
    df["sales"] = (
        0.3 * df["tv_spend"]
        + 0.5 * df["digital_spend"]
        + 0.2 * df["radio_spend"]
        + np.random.normal(0, 20, size=n)
    )
 
    # Add some missing values
    df.loc[5:10, "tv_spend"] = np.nan
    df.loc[20:25, "radio_spend"] = np.nan
 
    return df
 
 
def run_eda():
    """Run full EDA pipeline."""
 
    print("Creating sample data...")
    df = create_sample_data()
 
    print("Running OwlMix EDA...")
 
    eda = OwlMixEDA(
        df,
        target="sales",
        output_dir="outputs"
    )
 
    # Generate text report
    report = eda.report(include_charts=True, save=True)
 
    print("\nTEXT REPORT PREVIEW:\n")
    print(report[:500])  # print first 500 chars
 
    # Generate HTML report
    html = eda.to_html(save=True)
 
    print("\nHTML report generated!")
 
    print("\nCheck the following:")
    print(" - outputs/eda_report.txt")
    print(" - outputs/eda_report.html")
    print(" - outputs/charts/")
 
    print("\nDone!")
 
 
if __name__ == "__main__":
    run_eda()
 