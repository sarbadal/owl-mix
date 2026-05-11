import os, sys
import warnings
from pathlib import Path

warnings.simplefilter('ignore', category=UserWarning)

# Add src to the path
CURRENT_DIR = Path(__file__).parent.parent
SRC_DIR = CURRENT_DIR / "src"
sys.path.append(str(SRC_DIR))

#===============================================================================
import pandas as pd
from owlmix.utils.sample_data_generator import create_sample_data
from owlmix.reporting.report_builder import ReportBuilder
# import owlmix.reporting.sections


def test_acf_pacf_report_generation():
    df = create_sample_data(n=500)
    report_builder = ReportBuilder(
        df=df,
        target_col="sales",
        date_col="time"
    )

    # report_builder.add_section_by_name("acf_pacf")

    # report_builder.config.update_acf_pacf_config(
    #     columns=["sales"],
    #     n_lags=20,
    #     precision=4
    # )

    # report_builder.config.update_config(
    #     acf_pacf_config={
    #         "columns": ["sales"],
    #         "n_lags": 25,
    #         "precision": 3
    #     }
    # )


    report = report_builder.build()
    # print(report)

    report_builder.save("result.json")

if __name__ == "__main__":
    test_acf_pacf_report_generation()