# 🦉 OwlMix

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Docs](https://readthedocs.org/projects/owl-mix/badge/?version=latest)](https://owl-mix.readthedocs.io/)
[![PyPI version](https://img.shields.io/pypi/v/owl-mix/)](https://pypi.org/project/owl-mix/)

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

### Load Config from Dict, YAML, or JSON

You can load report section config using a Python dictionary, a YAML file, or a JSON file.

```python
from owlmix.reporting import ReportBuilder

report_builder = ReportBuilder(
    df=df,
    target_col="kpi",
    date_col="date"
)

# 1) From Python dict
config_dict = {
    "acf_pacf": {
        "columns": ["kpi"],
        "n_lags": 10,
        "precision": 2
    },
    "ccf": {
        "feature_columns": ["tv_spend", "digital_spend"],
        "max_lag": 3
    }
}
report_builder.config.update_config_from_dict(config_dict, strict=True)

# 2) From YAML file
report_builder.config.update_config_from_yaml("report_config.yaml", strict=True)

# 3) From JSON file
report_builder.config.update_config_from_json("report_config.json", strict=True)
```

Notes:

- `strict=True` raises an error if unknown section keys are present.
- Supported top-level section keys include: `acf_pacf`, `vif`, `correlation`, `causality`, `box_plot`, `ccf`, `response_curve`, `response_summary`, `dist_numeric`, and `time_series`.
- YAML/JSON must have a dictionary at the top level, and each section value must also be a dictionary.

### Installation

```sh
pip install owl-mix
```

### Documentation

- [Full Documentation](https://owl-mix-dev.readthedocs.io)
