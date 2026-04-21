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
import random

# from owlmix.report.generator import OwlMixReport
from owlmix.report import OwlMixReport

from owlmix.utils.distribution_data_generator import CategoryDistributionGenerator

colors: list[str] = [
    "#1f77b4",  # muted blue
    "#ff7f0e",  # safety orange
    "#2ca02c",  # cooked asparagus green
    "#d62728",  # brick red
    "#9467bd",  # muted purple
    "#8c564b",  # chestnut brown
    "#e377c2",  # raspberry yogurt pink
    "#7f7f7f",  # middle gray
    "#bcbd22",  # curry yellow-green
    "#17becf",  # blue-teal
    "#aec7e8",  # light blue
    "#ffbb78",  # light orange
    "#98df8a",  # light green
    "#ff9896",  # light red
    "#c5b0d5",  # light purple
    "#c49c94",  # light brown
    "#f7b6d2",  # light pink
    "#c7c7c7",  # light gray
    "#dbdb8d",  # light yellow-green
    "#9edae5",  # light blue-teal
]

smartphones = [
    "Apple iPhone 17 Pro",
    "Apple iPhone 16 Plus",
    "Samsung Galaxy S25 Ultra",
    "Samsung Galaxy S25 FE",
    "Samsung Galaxy Z Fold7",
    "Google Pixel 10 Pro XL",
    "OnePlus 15 5G",
    "OnePlus 13",
    "Xiaomi 17 Ultra",
    "Xiaomi Redmi Note 15",
    "Vivo X300 Pro",
    "Nothing Phone (3a) Lite",
    "Motorola Edge 70 Fusion",
    "Realme GT 8 Pro",
    "iQOO 15 Apex"
]

car_models = [
    "Toyota Corolla",
    "Honda Civic",
    "Ford F-150",
    "Tesla Model 3",
    "BMW M4",
    "Mercedes-Benz C-Class",
    "Porsche 911",
    "Hyundai Tucson",
    "Kia Sportage",
    "Volkswagen Golf",
    "Audi Q5",
    "Chevrolet Silverado",
    "Mazda CX-5",
    "Subaru Outback",
    "Land Rover Defender"
]

popular_languages = [
    "Python",
    "JavaScript",
    "Java",
    "C#",
    "C++",
    "TypeScript",
    "PHP",
    "Go",
    "Rust",
    "Swift",
    "SQL",
    "Kotlin",
    "Ruby",
    "R",
    "Dart",
    "Scala",
    "Shell",
    "Objective-C",
    "Perl",
    "Haskell",
    "Lua",
    "Elixir",
    "MATLAB",
    "Solidity",
    "Julia",
    "Clojure",
    "Groovy",
    "F#",
    "Erlang",
    "Fortran",
    "Cobol",
    "VHDL"
]


def create_sample_data(n=100):
    """Create sample MMM-like dataset."""
    # np.random.seed(46)
 
    dates = pd.date_range(start="2021-01-01", periods=n, freq="D")
    colors_ = CategoryDistributionGenerator(colors).generate(n_samples=n, sigma=0.5)
    smartphones_ = CategoryDistributionGenerator(smartphones).generate(n_samples=n, sigma=0.5)
    car_models_ = CategoryDistributionGenerator(car_models).generate(n_samples=n, sigma=0.5)
    languages_ = CategoryDistributionGenerator(popular_languages).generate(n_samples=n, sigma=0.5)
 
    df = pd.DataFrame({
        "time": dates,
        "tv_spend": np.random.randint(100, 500, size=n),
        "digital_spend": np.random.randint(50, 300, size=n),
        "radio_spend": np.random.randint(20, 150, size=n),
        "tv_grp": np.random.randint(10, 100, size=n),
        "radio_grp": np.random.randint(20, 150, size=n),
        "digital_imp": np.random.randint(10, 100, size=n),
        "radio_imp": np.random.randint(20, 150, size=n),
        "inflation": np.random.randint(10, 100, size=n),

        "color": colors_,
        "smartphone": smartphones_,
        "car_model": car_models_,
        "language": languages_,
    })

    df['time'] = df['time'].dt.strftime("%Y-%m-%d")
 
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
    df = create_sample_data(n=2365)
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
    )

    report.set_categorical_columns(
        columns=["color", "smartphone", "car_model", "language"]
    )

    # report.set_vif_config(
    #     features=["tv_spend", "digital_spend", "radio_spend"],
    #     precision=5,
    # )

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
        json_file_name="report_custom.json",
        html_file_name="report_custom.html",
    )


if __name__ == "__main__":
    main()