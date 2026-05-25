import warnings
import sys

sys.dont_write_bytecode = True
warnings.simplefilter('ignore', category=UserWarning)

import pandas as pd
from owlmix.utils.sample_data_generator import create_sample_data
from owlmix.reporting import ReportBuilder, ReportHTMLRenderer
from owlmix.typing.enums import SectionEnum


def render_html_report_from_json():
    report_json_path = "outputs/report.json"
    saved_html_path = "outputs/report.html"
    
    renderer = ReportHTMLRenderer()
    html_str = renderer.render_from_json(report_json_path)
    renderer.save_html(html_str, saved_html_path)


def main():
    df = create_sample_data(n=300, include_nan=False)

    report_builder = ReportBuilder(
        df=df,
        target_col="sales",
        date_col="time"
    )

    # This is an another way to update the config for a specific section, you 
    # can also update the config for all sections at once by passing a 

    # dictionary to the update_config method.
    # report_builder.config.update_acf_pacf_config(
    #     columns=["sales"],
    #     n_lags=20,
    #     precision=2
    # )

    report_builder.config.update_config(
        acf_pacf={
            "columns": ["digital_imp", "radio_spend"],  # , "tv_spend", "digital_imp", "radio_spend"],
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

    report_builder.add_output_dir("outputs")
    report = report_builder.build(
        with_all_sections=True,
        verbose=True,
    )

    report_builder.save("report.json")

if __name__ == "__main__":
    main()
    render_html_report_from_json()