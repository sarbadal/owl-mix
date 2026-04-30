import os, sys
import warnings
from pathlib import Path

warnings.simplefilter('ignore', category=UserWarning)

# Add src to the path
CURRENT_DIR = Path(__file__).parent.parent
SRC_DIR = CURRENT_DIR / "src"
sys.path.append(str(SRC_DIR))

# This test script is designed to manually test the OwlMixReport class from the owlmix.report.generator module.
# It creates a sample DataFrame, initializes the report generator, and tests the JSON and HTML
import pandas as pd
import random
from owlmix.report.generator import OwlMixReport

def get_sample_df():
    # Create a simple DataFrame for testing
    data = {
        "date": pd.date_range(start="2023-01-01", periods=50, freq="D"),
        "target": [random.randint(10, 20) for _ in range(50)],
        "tv_grp": [random.randint(1, 10) for _ in range(50)],
        "radio_grp": [random.randint(2, 8) for _ in range(50)],
        "tv_spend": [random.randint(100, 1000) for _ in range(50)],
    }
    return pd.DataFrame(data)

def main():
    df = get_sample_df()
    report = OwlMixReport(
        df=df,
        target="target",
        date_column="date",
        # Optionally, set user_title_config_path or other kwargs here
    )

    vif_color_rules = [
        (2, "blue"),
        (3.5, "green"),
        (5, "yellow"),
        (7, "orange"),
        (10, "red"),
        (float("inf"), "darkred")
    ]

    # report.config.update_vif_config(color_thresholds=vif_color_rules)

    # Test generate_json
    # report_dict, json_path = report.generate_json(
    #     out_file_name="manual_test_report.json"
    # )
    # print(f"JSON report generated at: {json_path}")

    # Test generate_html
    html_path = report.generate_html(
        out_file_name="manual_test_report.html",
        # save_json=True,
    )
    print(f"HTML report generated at: {html_path}")

    # Test run (should generate both)
    # report.run(
    #     json_file_name="manual_test_report_run.json",
    #     html_file_name="manual_test_report_run.html"
    # )
    # print("Run method executed. Check outputs directory for files.")

if __name__ == "__main__":
    main()