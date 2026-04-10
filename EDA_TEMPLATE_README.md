# OwlMix EDA Report Template

This directory contains a Jinja2 HTML template for generating professional EDA (Exploratory Data Analysis) reports for Marketing Mix Modeling.

## Files

- `eda_report_template.html` - The Jinja2 template
- `eda_report_formatted.html` - A static example of the rendered report
- `generate_eda_report.py` - Python script showing how to use the template

## Template Variables

The template expects the following data structure:

### Required Variables

#### `dataset_info` (dict)
- `rows` (int): Number of records in the dataset
- `columns` (int): Number of columns in the dataset
- `date_range` (dict, optional): Date range information
  - `start` (str): Start date
  - `end` (str): End date

#### `missing_values` (dict)
- Key: Column name (str)
- Value: Number of missing values (int)

#### `columns` (list)
- List of column names in the order they should appear in the statistics table

#### `descriptive_stats` (dict)
- Key: Statistic name (e.g., "count", "mean", "min", "25%", "50%", "75%", "max", "std")
- Value: Dictionary mapping column names to their statistic values

#### `charts` (list)
- List of chart objects, each containing:
  - `title` (str): Chart title
  - `description` (str): Chart description
  - `image_src` (str): Path to the chart image
  - `alt_text` (str): Alt text for the image

### Optional Variables

#### Header Customization
- `title` (str): Page title (default: "OwlMix EDA Report")
- `header_title` (str): Main header title (default: "🦉 OwlMix EDA Report")
- `header_subtitle` (str): Header subtitle (default: "Exploratory Data Analysis for Marketing Mix Modeling")

#### Footer
- `generator` (str): Generator name (default: "OwlMix EDA Module")
- `report_date` (str): Report generation date (default: "Unknown")

## Usage Example

```python
from jinja2 import Template

# Load template
with open('eda_report_template.html', 'r') as f:
    template = Template(f.read())

# Prepare your data
data = {
    "dataset_info": {
        "rows": 1000,
        "columns": 8,
        "date_range": {"start": "2023-01-01", "end": "2023-12-31"}
    },
    "missing_values": {
        "date": 0,
        "sales": 5,
        "tv_spend": 10,
        # ... other columns
    },
    "columns": ["date", "sales", "tv_spend", "digital_spend", "radio_spend"],
    "descriptive_stats": {
        "count": {"date": 1000, "sales": 995, "tv_spend": 990, ...},
        "mean": {"sales": 150.5, "tv_spend": 250.0, ...},
        # ... other statistics
    },
    "charts": [
        {
            "title": "Correlation Matrix",
            "description": "Heatmap showing variable correlations...",
            "image_src": "correlation.png",
            "alt_text": "Correlation Matrix"
        },
        # ... other charts
    ],
    "report_date": "2024-01-15"
}

# Render template
html_output = template.render(**data)

# Save to file
with open('my_eda_report.html', 'w') as f:
    f.write(html_output)
```

## Data Preparation Tips

1. **Missing Values**: Use pandas `isnull().sum()` to get missing value counts
2. **Descriptive Statistics**: Use pandas `describe()` method and convert to the required format
3. **Date Range**: Extract min/max dates from your date column
4. **Charts**: Ensure image files are in the same directory or provide full paths

## Integration with OwlMix

This template is designed to work with the OwlMix EDA module. The `generate_eda_report.py` script shows how to integrate it with your existing EDA workflow.