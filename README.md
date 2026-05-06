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
- scikit-learn>=1.8.0
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

### Handling Categorical Variables

To get the most out of your analysis, it is essential to explicitly define your categorical columns. **If these are not set, OwlMix will not generate categorical distribution charts in the final report.**

### Why This Is Important
Explicitly defining categorical variables ensures that the OwlMix engine:
*   **Generates Visualizations:** Triggers the creation of frequency and distribution charts in the HTML output.
*   **Ensures Data Integrity:** Correctly interprets columns as discrete categories (e.g., `store_id` or `product_code`) even if they contain numerical values.

### Usage
Use the `update_categorical_columns_config` method after initializing your report object, but before calling `.run()`.

```python
import pandas as pd
from owlmix.report import OwlMixReport

# Load your data
df = pd.read_csv("data.csv")

# Initialize the report
report = OwlMixReport(
    df=df,
    target="sales",
    date_column="date"
)

# Define your categorical features
cat_cols = ["color", "smartphone", "car_model", "language"]

# Update the configuration
# Without this line, distribution charts for these columns will be skipped
report.config.update_categorical_columns_config(columns=cat_cols)

# Run the report
report.run(html_file_name="report.html")
```

> **Note:** If you find that specific charts are missing from your HTML report, double-check that the column names in your list exactly match the headers in your DataFrame.

---

### Customising Report Charts (Include, Exclude, & Reorder)

You can control exactly which visualisations appear in your report and the order in which they are displayed using the `summary_builder` attributes. This is useful for removing noise or prioritising the most important insights for your stakeholders.

### Chart Management Options
*   **Exclude**: Remove specific charts you don't need (e.g., removing Correlation if it's not relevant).
*   **Include**: Explicitly whitelist only the charts you want to see.
*   **Reorder**: Define a custom sequence for the charts in the HTML output.

### Usage
Use the `ChartID` enum to specify which charts to modify. These settings must be applied to `report.summary_builder` before calling `.run()`.

```python
from owlmix.report import OwlMixReport
from owlmix.typing.enums import ChartID

report = OwlMixReport(df=df, target="sales", date_column="time")

# 1. Exclude specific charts
report.summary_builder.exclude_charts = [
    ChartID.CORRELATION_CHART, 
    ChartID.COMPARISON_CHART
]

# 2. OR Include ONLY specific charts (Whitelisting)
# report.summary_builder.include_charts = [
#     ChartID.CORRELATION_CHART, 
#     ChartID.ACF_PACF_CHART
# ]

# 3. Reorder charts
# The report will follow the exact order of the list provided
report.summary_builder.reorder_charts = [
    ChartID.DISTRIBUTION_CHART,
    ChartID.TIME_SERIES_CHART,
    ChartID.CORRELATION_CHART
]

report.run(save_json=True)
```

### Key Rules
*   **Precedence**: If you set `include_charts`, OwlMix will prioritize that list and ignore exclusions outside of it.
*   **Enum Usage**: Always use the `ChartID` enum to reference charts to avoid string typos and ensure compatibility with future updates.

---

## Time based comparison table and chart

### ⚠️ Important Notes
 
- **YOY (week-level) can be tricky**
  - Some years have **53 weeks**, others have 52
  - ISO week numbering does not perfectly align with calendar dates
  - The same week number across years may represent slightly different date ranges
  - This can lead to **minor inconsistencies in YoY week comparisons**

### 📊 Supported Comparison Types
 
- **yoy_year**
  - Granularity: Year
  - Comparison: Current year vs previous year
 
- **mom**
  - Granularity: Month (`YYYY-MM`)
  - Comparison: Current month vs previous month
 
- **wow**
  - Granularity: Week (week start date)
  - Comparison: Current week vs previous week
 
- **qoq**
  - Granularity: Quarter (`YYYYQX`)
  - Comparison: Current quarter vs previous quarter
 
- **yoy_month**
  - Granularity: Month
  - Comparison: Same month across years (e.g., Jan 2024 vs Jan 2023)
 
- **yoy_quarter**
  - Granularity: Quarter
  - Comparison: Same quarter across years (e.g., Q1 2024 vs Q1 2023)
 
- **yoy_week**
  - Granularity: ISO Week
  - Comparison: Same week number across years

---

# OwlMix Configuration API Reference

OwlMix provides a comprehensive suite of `update_*` methods to fine-tune your analysis. These methods allow you to modify statistical parameters, chart aesthetics, and data processing logic.

### Implementation Pattern
All configuration updates must be performed on the `report.config` object **after** initialization and **before** calling `report.run()`.

```python
report = OwlMixReport(df=df, target="sales", date_column="date")

# Example: Chaining configuration updates
report.config.update_categorical_columns_config(columns=["brand", "store_id"]) \
             .update_correlation_config(method="pearson") \
             .update_acf_pacf_config(lags=40)
```

---

### Available Update Methods & Parameters


| Method | Description | Parameters (Keyword Arguments) |
| :--- | :--- | :--- |
| `update_categorical_columns_config` | **Essential:** Defines columns for categorical analysis. | `columns` |
| `update_time_series_config` | Configures the primary time series visualization. | `columns`, `model`, `period` |
| `update_time_aggregator_config` | Controls how data is grouped and aggregated. | `date_column`, `value_columns`, `agg_func`, `precision`, `freq` |
| `update_time_comparison_config` | Defines logic for PoP or YoY comparisons. | `date_column`, `value_columns`, `comparison_type`, `agg_func`, `precision`, `freq` |
| `update_time_comparison_chart_config`| Adjusts the visual layout of comparison charts. | `date_column`, `value_columns`, `comparison_type`, `agg_func`, `mode` |
| `update_correlation_config` | Sets parameters for correlation analysis. | `columns` |
| `update_correlation_chart_layout_config`| Customizes the heatmap UI and labels. | `columns` |
| `update_lag_corr_chart_config` | Configures cross-correlation with time lags. | `column` (required), `lag` |
| `update_acf_pacf_config` | Adjusts lags and markers for ACF/PACF plots. | `columns`, `n_lags`, `acf_marker`, `pacf_marker`, `acf_stem`, `pacf_stem`, `acf_conf`, `pacf_conf` |
| `update_distribution_chart_config` | Sets binning logic and chart grid layout. | `columns`, `max_charts_per_row` |
| `update_kpi_vs_feature_config` | Configures analysis of Target vs Features. | `target_column`, `columns`, `period`, `date_column`, `agg_func` |
| `update_causality_test_config` | Fine-tunes Granger causality test parameters. | `target_column`, `columns`, `max_lag`, `error_threshold`, `p_value_weight`, `mape_weight` |
| `update_vif_config` | Configures multicollinearity detection. | `target_column`, `features`, `precision`, `color_thresholds` |
| `update_outlier_chart_layout_config` | Adjusts outlier detection and visual markers. | `columns`, `max_cols_per_chart`, `single_image` |

### Quick Usage Tip
When passing values to these methods, ensure you use the argument names exactly as listed. For example:

```python
report.config.update_vif_config(
    features=["price", "inventory", "promotion"],
    precision=2
)
```

### Pro-Tips
*   **Method Chaining:** These methods return `self`, so you can chain multiple updates together for cleaner code.
*   **Validation:** If a chart is missing from your report, verify that its corresponding `update_` method has been called with the correct column names.
*   **Enums:** For methods like `update_correlation_config`, it is recommended to use the built-in `owlmix.typing.enums` to ensure parameter validity.


## Working with Enums

OwlMix uses **Enums** (Enumerations) to standardize configuration values. Using these instead of raw strings prevents typos and ensures your code remains compatible with future versions.

### Key Enum Reference Table


| Enum Class | Purpose | All Available Values |
| :--- | :--- | :--- |
| **`ChartID`** | Controlling chart visibility and order. | `VIF_CHART`, `ACF_PACF_CHART`, `KPI_VS_FEATURE_CHART`, `DISTRIBUTION_CHART`, `CATEGORICAL_DISTRIBUTION_CHART`, `CORRELATION_CHART`, `LAG_CORRELATION_CHART`, `TIME_SERIES_CHART`, `OUTLIERS_CHART`, `COMPARISON_CHART` |
| **`Period`** | Defining data aggregation frequency. | `DAILY`, `WEEKLY`, `MONTHLY`, `YEARLY` |
| **`ComparisonType`** | Setting logic for time-based comparisons. | `YoY`, `QoQ`, `MoM`, `WoW`, `YoY_MONTH`, `YoY_QUARTER`, `YoY_WEEK` |
| **`PlotMode`** | Choosing the visual axis/unit style. | `ABSOLUTE`, `PCT_CHANGE`, `DUAL` |

---

### Implementation Guide

#### Basic Usage
Always import the Enum classes from `owlmix.typing.enums`. 

```python
from owlmix.typing.enums import ChartID, ComparisonType, PlotMode

# Example: Filtering and Reordering
report.summary_builder.reorder_charts = [
    ChartID.TIME_SERIES_CHART,
    ChartID.COMPARISON_CHART,
    ChartID.CORRELATION_CHART
]

# Example: Setting Comparison Logic
report.config.update_time_comparison_config(
    comparison_type=ComparisonType.YoY_MONTH
)
```

#### Inspecting Enum Data
Since all Enums inherit from `BaseEnum`, you can programmatically inspect them if you are unsure of the underlying values or labels.

```python
# Returns a list of strings: ['DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']
print(Period.names())

# Returns a list of raw values: ['daily', 'weekly', 'monthly', 'yearly']
print(Period.values())

# Returns a formatted JSON string of IDs, Names, and Labels
print(ComparisonType.pretty_options())
```

> **Pro Tip:** Use `.label` if you need the human-readable version for your own custom logs or UI (e.g., `ComparisonType.YoY.label` returns `"Year over Year"`).

---


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
- `docs/include_exclude_reorder_charts.md` → Include Exclude and Reorder charts

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
 