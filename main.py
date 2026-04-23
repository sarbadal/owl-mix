import sys
import os
 
# --------------------------------------------------
# Add src/ to path (so we can import owlmix locally)
# --------------------------------------------------
CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.join(CURRENT_DIR, "src")
 
sys.path.insert(0, SRC_PATH)

# from owlmix.report.generator import OwlMixReport
from owlmix.report import OwlMixReport
from owlmix.utils.sample_data_generator import create_sample_data


def main():
    df = create_sample_data(n=1231)
    # df = pd.read_csv("tests/data/national_all_channels.csv")
    report = OwlMixReport(
        df,
        # target="revenue_per_conversion",
        # date_column="time",
        target="sales",
        date_column="time",
        # template_name="bootstrap_eda_template.html",
        template_name="custom_eda_template.html",
        # template_name="custom_eda_template_dark.html",
        # user_title_config_path="/Users/sarbadal.pal/Library/CloudStorage/OneDrive-OneWorkplace/PythonProjects/Canadian_Tire/owlmix/usr_config/title.json"
        user_title_config_path="usr_config/title.json"
    )

    report.config.set_time_aggregator_config(
        freq="ME",
        precision=4
    )

    report.config.set_categorical_columns_config(
        columns=[
            "color",
            "smartphone",
            "car_model",
            "language"
        ]
    )

    report.config.set_kpi_vs_feature_config(
        columns=["tv_spend", "digital_spend", "radio_spend"],
        date_format="%Y-%m",
    )

    report.config.set_vif_config(
        features=[
            "tv_spend",
            "digital_spend",
            "radio_spend",
            "tv_grp",
            "radio_grp",
            "digital_imp",
            # "sales",
        ],
        precision=2,
    )

    report.config.set_acf_pacf_config(
        columns=[
        #     "tv_spend",
        #     "digital_spend",
        #     "radio_spend",
        #     "tv_grp",
        #     "radio_grp",
        #     "digital_imp",
            "sales",
        ],
        n_lags=20
    )

    report.config.set_causality_test_config(
        max_lag=5,
        error_threshold=0.15
    )

    # report.set_time_comparison_config(
    #     date_column="date",
    #     value_columns=["tv_spend", "digital_spend", "radio_spend", "sales"],
    #     precision=3,
    # )

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
    report.run(
        json_file_name="report_custom_23_apr_26.json",
        html_file_name="report_custom_23_apr_26.html",
    )


if __name__ == "__main__":
    main()