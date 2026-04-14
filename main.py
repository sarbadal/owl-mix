import sys
import os
 
# --------------------------------------------------
# Add src/ to path (so we can import owlmix locally)
# --------------------------------------------------
CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.join(CURRENT_DIR, "src")
 
sys.path.insert(0, SRC_PATH)

import pandas as pd
import numpy as np

from owlmix.report.generator import OwlMixReport

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


def main():
    df = create_sample_data()
    report = OwlMixReport(
        df,
        target="sales",
        template_name="custom_eda_template.html"
    )
    report.run()


if __name__ == "__main__":
    main()