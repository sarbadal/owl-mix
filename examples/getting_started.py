from owlmix.report.generator import OwlMixReport
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

    # If no categorical columns are specified, no categorical analysis will be included in the report.
    report.config.update_categorical_columns_config(columns=categorical_columns)

    # run method will generate both JSON and HTML reports. You can specify file names or use defaults.
    # The html and JSON files will be available in outputs folder after running the code. 
    # You can open the HTML file in a browser to view the report.
    report.run(
        # Optionally, specify file names for the generated report. 
        # Defaults are report.json and report.html
        json_file_name="report_eda.json",
        html_file_name="report_eda.html"
    )

if __name__ == "__main__":    
    main()
