# 🦉 OwlMix

**OwlMix** is a comprehensive Python package for Exploratory Data Analysis (EDA) and data transformation tailored for **Marketing Mix Modeling (MMM)** workflows. It provides automated report generation, statistical analysis, and data transformation utilities to accelerate MMM projects.

---

## 🚀 Key Features

### 📊 **Data Analysis & Reporting**
- **Automated EDA Reports**: Generate professional HTML and JSON reports with comprehensive statistics and visualizations
- **Correlation Analysis**: Matrix correlations, lag correlations, and ACF/PACF analysis for time series
- **VIF Calculation**: Variance Inflation Factor detection for multicollinearity assessment
- **Causality Testing**: Granger causality tests to identify causal relationships
- **Categorical Analysis**: Distribution analysis for categorical variables
- **KPI vs Features**: Analyze relationships between KPIs and marketing features by time period
- **Time Series Decomposition**: Seasonal decomposition and trend analysis
- **Outlier Detection**: Visual identification and analysis of outliers

### 🔧 **Data Transformation**
- **Adstock Effect**: Apply advertising carryover effects to media spend data
- **Lag Generation**: Create lagged features for time series modeling
- **Saturation Transformation**: Apply saturation curves (Hill, Logistic, Logit) to media variables
- **Data Cleanup**: Automated data quality checks and handling (missing values, duplicates, etc.)
- **Transformation Pipeline**: Chainable pipeline for complex data workflows

### 🎨 **Visual & Export Options**
- **Multiple HTML Templates**: Light and dark theme templates for reports
- **Interactive Charts**: Distribution plots, time series, correlation heatmaps, outlier charts
- **JSON Export**: Raw report data for programmatic access
- **Chart Storage**: Automatic chart generation and storage in `outputs/charts/`

### ⚙️ **Flexible Configuration**
- Fine-grained control over analyses to include/exclude
- Customizable precision, date formats, and aggregation frequencies
- Column-specific configurations for targeted analysis
- Template customization support

---

## 📦 Installation

```bash
pip install owl-mix
```

**Requirements:**
- Python >= 3.12
- pandas >= 1.5
- matplotlib >= 3.7
- seaborn >= 0.12
- statsmodels >= 0.14.6
- scipy >= 1.10
- Jinja2 >= 3.1

---

## ⚡ Quick Start

### Basic EDA Report Generation

```python
import pandas as pd
from owlmix.report import OwlMixReport

# Load your data
df = pd.read_csv("your_data.csv")

# Create and generate report
report = OwlMixReport(
    df=df,
    target="sales",              # Target variable for analysis
    date_column="date",          # Date column for time series analysis
    template_name="custom_eda_template.html"  # Optional: use "custom_eda_template_dark.html" for dark theme
)

# Generate HTML and JSON reports
report.run(
    json_file_name="eda_report.json",
    html_file_name="eda_report.html"
)
```

**Output:**
- `eda_report.json`: Structured analysis data in JSON format
- `eda_report.html`: Interactive HTML report with charts and statistics
- `outputs/charts/`: Generated visualization files

---

## 🛠️ Advanced Configuration

### Customize Analyses

```python
import pandas as pd
from owlmix.report import OwlMixReport

df = pd.read_csv("your_data.csv")

report = OwlMixReport(
    df=df,
    target="sales",
    date_column="date"
)

# Configure time aggregation
report.config.set_time_aggregator_config(
    freq="ME",      # Month-end aggregation
    precision=4     # Decimal precision
)

# Configure categorical columns
report.config.set_categorical_columns_config(
    columns=["product_type", "region", "channel"]
)

# Configure KPI vs Feature analysis
report.config.set_kpi_vs_feature_config(
    columns=["tv_spend", "digital_spend", "radio_spend"],
    date_format="%Y-%m"
)

# Configure VIF (Variance Inflation Factor) analysis
report.config.set_vif_config(
    features=["tv_spend", "digital_spend", "radio_spend"],
    precision=2
)

# Configure ACF/PACF analysis
report.config.set_acf_pacf_config(
    columns=["sales", "digital_spend"],
    n_lags=20
)

# Configure causality testing
report.config.set_causality_test_config(
    max_lag=5,
    error_threshold=0.15
)

report.run(
    json_file_name="report.json",
    html_file_name="report.html"
)
```

### Data Transformation Pipeline

```python
from owlmix.transform import MMMTransformPipeline

# Create transformation pipeline
pipeline = MMMTransformPipeline(df, date_column="date")

# Apply transformations
pipeline.adstock(
    columns=["tv_spend", "digital_spend"],
    decay_rate=0.5,
    window=4
)

pipeline.create_lags(
    columns=["sales"],
    lags=[1, 2, 4, 13]
)

pipeline.saturation(
    columns=["tv_spend", "digital_spend"],
    method="hill",
    k_values=[100, 200]
)

pipeline.cleanup(
    handle_missing="mean",
    remove_duplicates=True
)

# Get transformed data
transformed_df = pipeline.get_data()
```

### Configuration Management with File Resolver

The `ConfigFileResolver` utility simplifies managing configuration files by automatically resolving file references in JSON configs. This is useful for keeping configuration data organized across multiple files.

```python
from owlmix.file_resolver import ConfigFileResolver

# Create a resolver with a JSON config file
resolver = ConfigFileResolver(config="config.json")

# Resolve *_file keys to their actual content
resolved_config = resolver.resolve()

# Save the resolved config
resolver.save("resolved_config.json")

# Get as Python dictionary string
python_dict_string = resolver.to_python_string()
print(python_dict_string)

# Print formatted output
resolver.print()
```

**How it works:**
- Any JSON key ending with `_file` is automatically resolved to the file's content
- Supports any file type (HTML, TXT, MD, JSON, etc.)
- Works recursively through nested dictionaries and lists
- Includes built-in caching for efficiency

**Example Configuration:**

```json
{
    "report_template": {
        "description_file": "templates/report_description.html",
        "title": "Analysis Report",
        "metadata_file": "config/metadata.json"
    }
}
```

After resolution, `description_file` key becomes `description` with the HTML file's content, and `metadata_file` becomes `metadata` with the JSON content.

---

## 📊 Report Sections

The generated HTML report includes comprehensive sections:

| Section | Description |
|---------|-------------|
| **Dataset Overview** | Basic information, data types, missing values, memory usage |
| **Summary Statistics** | Descriptive statistics (mean, std, min, max, quantiles) |
| **Data Quality** | Missing value patterns, duplicate analysis |
| **Distributions** | Histograms and density plots for all numeric variables |
| **Outlier Analysis** | Box plots and outlier identification |
| **Correlation Matrix** | Pairwise correlations with heatmap visualization |
| **Lag Correlations** | Time-lagged correlation analysis for time series |
| **VIF Analysis** | Multicollinearity detection using Variance Inflation Factor |
| **ACF/PACF** | Autocorrelation and partial autocorrelation for seasonality detection |
| **Causality Tests** | Granger causality tests for causal relationships |
| **Time Comparisons** | Period-over-period comparisons (YoY, MoM) |
| **KPI vs Features** | Relationship between target and marketing features over time |
| **Categorical Distributions** | Distribution analysis for categorical variables |

---

## 🔧 Core Modules

### `owlmix.eda`
Exploratory Data Analysis module with:
- `EDAAnalyzer`: Core statistical analysis engine
- `SummaryBuilder`: Comprehensive summary generation
- `OwlMixEDA`: Main EDA orchestrator

**Features:**
- Correlation analysis (matrix, lag, causality)
- VIF calculation for multicollinearity
- ACF/PACF analysis for seasonality
- Categorical and distribution analysis
- Outlier detection and visualization

### `owlmix.transform`
Data transformation module for MMM preprocessing:
- `adstock()`: Apply advertising carryover effects
- `create_lags()`: Generate lagged features
- `saturation()`: Apply saturation curves (Hill, Logistic, Logit)
- `cleanup_data()`: Data quality utilities
- `MMMTransformPipeline`: Chainable pipeline for complex workflows

### `owlmix.report`
Report generation module:
- `OwlMixReport`: Main report generator
- HTML template rendering with customizable themes
- JSON data export
- Chart generation and storage

---

## 📈 Example Use Cases

### Marketing Mix Modeling Workflow
```python
import pandas as pd
from owlmix.report import OwlMixReport
from owlmix.transform import MMMTransformPipeline

# Load raw data
df = pd.read_csv("mmm_data.csv")

# Step 1: Transform data
pipeline = MMMTransformPipeline(df, date_column="date")
pipeline.adstock(columns=["tv", "digital", "radio"], decay_rate=0.5)
pipeline.create_lags(columns=["sales"], lags=[1, 4, 13])
df_transformed = pipeline.get_data()

# Step 2: Analyze with EDA
report = OwlMixReport(
    df=df_transformed,
    target="sales",
    date_column="date"
)
report.config.set_vif_config(
    features=["tv", "digital", "radio"],
    precision=3
)
report.run(
    json_file_name="mmm_eda.json",
    html_file_name="mmm_eda.html"
)
```

---

## 📚 Documentation

- [EDA Documentation](src/owlmix/docs/eda.md)
- [Transform Documentation](src/owlmix/docs/transform.md)
- [Saturation Curves](src/owlmix/docs/saturation.md)

---

## 💡 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues on [GitHub](https://github.com/sarbadal/owl-mix).

---

## 📄 License

MIT License - see LICENSE file for details

**Author:** Sarbadal Pal (sarbadal@gmail.com)

**Repository:** [github.com/sarbadal/owl-mix](https://github.com/sarbadal/owl-mix)

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
 