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
from owlmix.typing.enums import SectionEnum


def test_render_html_report_from_json():
    renderer = ReportHTMLRenderer()
    html_str = renderer.render_from_json(CURRENT_DIR / "tests/output/result.json")
    renderer.save_html(html_str, CURRENT_DIR / "tests/output/report.html")


def test_report_generation():
    df = create_sample_data(n=300, include_nan=False)
    # print(df)

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
            "columns": ["sales", "digital_imp", "radio_spend"],  # , "tv_spend", "digital_imp", "radio_spend"],
            "n_lags": 10,
            "precision": 2
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
            "columns": ["tv_spend", "digital_spend", "radio_spend", "tv_grp", "digital_imp"],
            "n_plot_per_row": 5,
            "method": "zscore",
            "threshold": 1.7 # default is 3 for method "zscore" and 1.5 for method "iqr"
        },
        ccf={
            "feature_columns": [
                "tv_spend",
                "digital_spend",
                # "radio_spend",
                # "tv_grp",
                # "digital_imp"
            ],
            "max_lag": 3
        },
        response_curve={
            "feature_columns": ["tv_spend", "digital_spend", "radio_spend", "tv_grp", "digital_imp"],
            "target_column": "sales",
        },
        response_summary={
            "feature_columns": ["tv_spend", "digital_spend", "radio_spend", "tv_grp", "digital_imp"],
            "target_column": "sales",
        },
    )

    # report_builder.add_all_sections(verbose=True)
    # report_builder.exclude_sections([SectionEnum.CAUSALITY, "ccf"], verbose=True)
    # report_builder.include_sections([SectionEnum.CAUSALITY, "ccf"], verbose=True)

    # report_builder.add_section_by_name("acf_pacf", verbose=True)
    # report_builder.add_section_by_name("vif", verbose=True)

    report = report_builder.build(
        with_all_sections=True,
        verbose=True,
    )
    # print(report)

    report_builder.save("result.json")

if __name__ == "__main__":
    # test_report_generation()
    test_render_html_report_from_json()