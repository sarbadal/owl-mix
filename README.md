# 🦉 OwlMix

**OwlMix** is a Python library for automated exploratory data analysis (EDA), 
designed for time-series and marketing mix modeling (MMM) workflows. OwlMix helps 
you quickly understand your data, identify trends, and prepare for modeling.

### Features

- Automated EDA report generation (HTML/JSON)
- Time series lag and correlation analysis
- Variable relationship and distribution insights
- Causality and trend detection
- Easy-to-use API

### Quick Start

```python
import pandas as pd
from owlmix.reporting import ReportBuilder, ReportHTMLRenderer

csv_file = "path/to/your/csv/file.csv"

df = pd.read_csv(csv_file)
report_builder = ReportBuilder(
    df=df, 
    target_col="kpi", 
    date_col="date"
)

# Update the config, if needed
report_builder.config.update_config(
    acf_pacf={
        "columns": ["kpi"],
        "n_lags": 5
    },
    vif={
        "features": ["tv_spend", "digital_spend", "radio_spend"]
    },
    correlation={
        "columns": ["kpi", "tv_spend"],
        "n_lags": 8,
        "precision": 5
    },
    box_plot={
        "columns": ["kpi", "tv_spend", "digital_spend", "radio_spend", "tv_grp", "digital_imp"],
        "n_plot_per_row": 3,
        "method": "zscore",
        "threshold": 1.5  # default is 3 for method "zscore" and 1.5 for method "iqr"
    },
    ccf={
        "feature_columns": ['tv_spend'],
        "max_lag": 3
    },
    # update the other configs
)
report_builder.add_all_sections(verbose=True)
report = report_builder.build()
report_builder.save("result.json")

renderer = ReportHTMLRenderer()
html_str = renderer.render_from_json("result.json")
renderer.save_html("report.html")
```

### Installation

```sh
pip install owl-mix
```

### Documentation

- [Full Documentation](https://owl-mix-dev.readthedocs.io)
