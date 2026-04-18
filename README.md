# 🦉 OwlMix

**OwlMix** is a Python package for generating comprehensive Exploratory Data Analysis (EDA) reports tailored for Marketing Mix Modeling (MMM) workflows.

It helps data scientists and analysts quickly generate HTML and JSON reports with dataset summaries, correlations, charts, and more.

---

## 🚀 Key Features

- **Automated EDA Reports**: Generate detailed HTML reports with charts and statistics
- **Correlation Analysis**: Matrix and lag correlations for time series data
- **VIF Calculation**: Variance Inflation Factor for multicollinearity detection
- **Time Series Comparisons**: Year-over-year and other time-based comparisons
- **Visual Charts**: Distribution, outliers, time series, and correlation plots
- **Flexible Configuration**: Customize which analyses and charts to include
- **Export Options**: Both HTML and JSON outputs

---

## 📦 Installation

```bash
pip install owlmix
```

---

## ⚡ Quick Start

```python
import pandas as pd
from owlmix.report import OwlMixReport

# Load your data
df = pd.read_csv("your_data.csv")

# Create and run the report
report = OwlMixReport(
    df=df,
    target="sales",  # Your target variable
    date_column="date",  # Date column name
    template_name="custom_eda_template.html"  # Optional: use dark theme with "custom_eda_template_dark.html"
)

# Generate both JSON and HTML reports
report.run(
    json_file_name="eda_report.json",
    html_file_name="eda_report.html"
)
```

This will create:
- `eda_report.json`: Raw data in JSON format
- `eda_report.html`: Beautiful HTML report with charts
- `outputs/charts/`: Generated chart images

---

## 🛠️ Customization

Configure what to include in your report:

```python
report = OwlMixReport(df, target="sales", date_column="date")

# Customize VIF analysis
report.set_vif_config(
    features=["tv_spend", "digital_spend", "radio_spend"],
    precision=3
)

# Customize time comparisons
report.set_time_comparison_config(
    value_columns=["sales", "tv_spend"],
    comparison_type="yoy",
    precision=2
)

# Customize charts
report.set_outlier_chart_layout(
    columns=["sales", "tv_spend"],
    max_cols_per_chart=4
)

report.run()
```

---

## 📊 Report Sections

The generated HTML report includes:

- **Dataset Overview**: Basic info, data types, missing values
- **Summary Statistics**: Descriptive stats for all variables
- **Correlation Matrix**: Pairwise correlations
- **VIF Analysis**: Multicollinearity detection
- **Time Comparisons**: Period-over-period changes
- **Visualizations**: Charts for distributions, outliers, time series, etc.

---

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

- `docs/eda.md` → EDA module details
- `docs/transform.md` → Data transformation features
- `docs/saturation.md` → Saturation modeling

---

## 🧪 Examples

Ready-to-run examples in the `examples/` folder:

- `eda_basic.py` - Basic EDA report generation
- `eda_full_workflow.py` - Complete workflow example
- `mmm_workflow_example.py` - Marketing Mix Modeling example

---

## 🧠 Use Case: Marketing Mix Modeling

OwlMix is designed for MMM workflows where you need to:

1. **Explore** relationships between marketing spend and sales
2. **Identify** multicollinearity issues with VIF
3. **Analyze** time-based patterns and correlations
4. **Generate** professional reports for stakeholders

Perfect for preprocessing data before building MMM models!
 
Owl Mix is particularly useful for:
 
- Preprocessing marketing data
- Feature engineering for MMM
- Understanding lagged media effects
- Generating EDA reports before modeling
 
---
 
## 🔧 Roadmap
 
Planned enhancements:
 
- Visualization support (plots, heatmaps)
- HTML report generation
- Automated MMM diagnostics
- CLI support
 
---
 
## 🤝 Contributing
 
Contributions are welcome!
 
Feel free to:
- Open issues
- Suggest features
- Submit pull requests
 
---
 
## 📄 License
 
This project is licensed under the MIT License.
 
---
 
## ⭐ Support
 
If you find this project useful, consider giving it a star ⭐ on GitHub!
 