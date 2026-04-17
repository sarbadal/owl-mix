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

# from owlmix.report.generator import OwlMixReport
from owlmix.report import OwlMixReport

def create_sample_data(n=100):
    """Create sample MMM-like dataset."""
    np.random.seed(42)
 
    dates = pd.date_range(start="2024-01-01", periods=n, freq="D")
 
    df = pd.DataFrame({
        "date": dates,
        "tv_spend": np.random.randint(100, 500, size=n),
        "digital_spend": np.random.randint(50, 300, size=n),
        "radio_spend": np.random.randint(20, 150, size=n),
        "tv_grp": np.random.randint(10, 100, size=n),
        "radio_grp": np.random.randint(20, 150, size=n),
        "digital_imp": np.random.randint(10, 100, size=n),
    })

    df['date'] = df['date'].dt.strftime("%Y-%m-%d")
 
    # Create synthetic sales with some relationship
    df["sales"] = (
        0.3 * df["tv_spend"]
        + 0.5 * df["digital_spend"]
        + 0.2 * df["radio_spend"]
        + 0.2 * df["tv_grp"]
        + 0.2 * df["radio_grp"]
        + 0.2 * df["digital_imp"]
        + np.random.normal(0, 20, size=n)
    )
 
    # Add some missing values
    df.loc[5:10, "tv_spend"] = np.nan
    df.loc[20:25, "radio_spend"] = np.nan
 
    return df


def main():
    df = create_sample_data(n=500)
    # df = pd.read_csv("tests/data/national_all_channels.csv")
    report = OwlMixReport(
        df,
        # target="revenue_per_conversion",
        # date_column="time",
        target="sales",
        date_column="date",
        template_name="custom_eda_template.html",
    )

    report.set_time_comparison_config(
        date_column="date",
        value_columns=["tv_spend", "digital_spend", "radio_spend", "sales"],
        precision=3,
    )

    # report.set_correlation_config(
    #     columns=["tv_spend", "radio_spend", "digital_spend"]
    # )

    # report.set_outlier_chart_layout(
    #     columns=["sales", "tv_spend", "radio_spend", "digital_spend"],
    #     max_cols_per_chart=5
    # )

    # report.set_correlation_chart_layout(
    #     columns=["sales", "tv_spend", "radio_spend", "digital_spend"],
    #     precision=1
    # )
    report.run()


if __name__ == "__main__":
    main()