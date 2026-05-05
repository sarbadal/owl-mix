from owlmix.report.generator import OwlMixReport
from owlmix.typing.enums import ChartID
from owlmix.utils.sample_data_generator import create_sample_data


def load_data(n=500) -> "pd.DataFrame":
    return create_sample_data(n=n)


def main() -> None:
    df: "pd.DataFrame" = load_data()
    categorical_columns = ["color", "smartphone", "car_model", "language"]

    report = OwlMixReport(
        df=df,
        target="sales",
        date_column="time",
        # Optionally, set user_title_config_path or other kwargs here
    )

    report.summary_builder.exclude_charts = [ChartID.CORRELATION_CHART, ChartID.COMPARISON_CHART]
    # report.summary_builder.include_charts = [ChartID.CORRELATION_CHART, ChartID.ACF_PACF_CHART]

    # If no categorical columns are specified, no categorical analysis will be included in the report.
    report.config.update_categorical_columns_config(columns=categorical_columns)

    report.run(save_json=True)

if __name__ == "__main__":    
    main()
