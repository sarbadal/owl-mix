import os, sys
import warnings
from pathlib import Path

from statsmodels.graphics import correlation

warnings.simplefilter('ignore', category=UserWarning)

# Add src to the path
CURRENT_DIR = Path(__file__).parent.parent
SRC_DIR = CURRENT_DIR / "src"
sys.path.append(str(SRC_DIR))

#===============================================================================
import pandas as pd
from owlmix.utils.sample_data_generator import create_sample_data
from owlmix.reporting import ReportBuilder, ReportHTMLRenderer
# from owlmix.reporting.report_builder import ReportBuilder
# import owlmix.reporting.sections


def test_render_html_report_from_json():
    renderer = ReportHTMLRenderer()
    html_str = renderer.render_from_json(CURRENT_DIR / "tests/output/result.json")
    renderer.save_html(html_str, CURRENT_DIR / "tests/output/report.html")


def test_report_generation():
    df = create_sample_data(n=500)
    report_builder = ReportBuilder(
        df=df,
        target_col="sales",
        date_col="time"
    )


    # report_builder.config.update_acf_pacf_config(
    #     columns=["sales"],
    #     n_lags=20,
    #     precision=2
    # )

    report_builder.config.update_config(
        acf_pacf={
            "columns": ["sales", "tv_spend"],
            "n_lags": 5,
            "precision": 3
        },
        vif={
            # "features": [
            #     "tv_spend",
            #     "digital_spend",
            #     "radio_spend"
            # ],
            "precision": 2
        },
        correlation={
            # "columns": ["sales", "tv_spend"],
            "n_lags": 8,
            "precision": 5
        },
        box_plot={
            "columns": ["sales", "tv_spend", "digital_spend"],
            "n_plot_per_row": 5,
            # "method": "zscore",
            # "threshold": 3
        }
    )

    report_builder.add_all_sections(verbose=True)

    # report_builder.add_section_by_name("acf_pacf")

    report = report_builder.build()
    # print(report)

    report_builder.save("result.json")

if __name__ == "__main__":
    test_report_generation()
    # test_render_html_report_from_json()