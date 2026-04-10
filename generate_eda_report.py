"""Example script showing how to use the Jinja2 EDA Report Template."""

from jinja2 import Template
import os
import base64

def image_to_base64(image_path):
    """
    Convert an image file to base64 data URI.

    Args:
        image_path (str): Path to the image file

    Returns:
        str: Base64 data URI string
    """
    if not os.path.exists(image_path):
        return ""

    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # Get file extension to determine MIME type
        ext = os.path.splitext(image_path)[1].lower()
        if ext == '.png':
            mime_type = 'image/png'
        elif ext == '.jpg' or ext == '.jpeg':
            mime_type = 'image/jpeg'
        elif ext == '.gif':
            mime_type = 'image/gif'
        elif ext == '.webp':
            mime_type = 'image/webp'
        else:
            mime_type = 'image/png'  # default

        return f'data:{mime_type};base64,{encoded_string}'

def generate_eda_report(template_path, output_path, data, images_base_path="outputs/"):
    """
    Generate an EDA report using the Jinja2 template.

    Args:
        template_path (str): Path to the HTML template file
        output_path (str): Path where the rendered HTML will be saved
        data (dict): Dictionary containing all the data to inject into the template
        images_base_path (str): Base path where images are located (default: "outputs/")
    """

    # Read the template
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Create Jinja2 template
    template = Template(template_content)

    # Render the template with data
    rendered_html = template.render(**data)

    # Write the rendered HTML to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

    print(f"EDA report generated successfully: {output_path}")

# Example data structure for the template
def get_sample_data(images_base_path="outputs/"):
    """Returns sample data that matches the template structure"""
    return {
        # Header customization
        "title": "OwlMix EDA Report",
        "header_title": "🦉 OwlMix EDA Report",
        "header_subtitle": "Exploratory Data Analysis for Marketing Mix Modeling",

        # Dataset information
        "dataset_info": {
            "rows": 100,
            "columns": 5,
            "date_range": {
                "start": "2023-01-01",
                "end": "2023-04-10"
            }
        },

        # Missing values (column_name: count)
        "missing_values": {
            "date": 0,
            "tv_spend": 6,
            "digital_spend": 0,
            "radio_spend": 6,
            "sales": 0
        },

        # Column names for the statistics table
        "columns": ["date", "tv_spend", "digital_spend", "radio_spend", "sales"],

        # Descriptive statistics (statistic_name: {column_name: value})
        "descriptive_stats": {
            "count": {"date": "-", "tv_spend": 94.0, "digital_spend": 100.0, "radio_spend": 94.0, "sales": 100.0},
            "mean": {"date": "2023-02-19", "tv_spend": 314.86, "digital_spend": 173.46, "radio_spend": 97.60, "sales": 199.58},
            "min": {"date": "2023-01-01", "tv_spend": 101.00, "digital_spend": 50.00, "radio_spend": 21.00, "sales": 81.02},
            "25%": {"date": "2023-01-25", "tv_spend": 212.00, "digital_spend": 100.00, "radio_spend": 67.75, "sales": 161.71},
            "50%": {"date": "2023-02-19", "tv_spend": 326.00, "digital_spend": 179.00, "radio_spend": 104.50, "sales": 197.78},
            "75%": {"date": "2023-03-16", "tv_spend": 408.75, "digital_spend": 244.00, "radio_spend": 132.00, "sales": 236.90},
            "max": {"date": "2023-04-10", "tv_spend": 489.00, "digital_spend": 299.00, "radio_spend": 149.00, "sales": 338.73},
            "std": {"date": "—", "tv_spend": 113.68, "digital_spend": 77.48, "radio_spend": 39.37, "sales": 52.92}
        },

        # Charts configuration
        "charts": [
            {
                "title": "Correlation Matrix",
                "description": "Heatmap displaying the correlation coefficients between all numerical variables. Values range from -1 (perfect negative correlation) to +1 (perfect positive correlation). This visualization helps identify which variables move together and which relationships may be useful for predictive modeling.",
                "image_data": image_to_base64(f"{images_base_path}/correlation.png"),
                "alt_text": "Correlation Matrix Heatmap"
            },
            {
                "title": "Time Series Trend Analysis",
                "description": "Line chart showing the temporal evolution of all variables across the study period (2023-01-01 to 2023-04-10). This visualization reveals trends, seasonality, and temporal patterns in marketing spend and sales performance over time.",
                "image_data": image_to_base64(f"{images_base_path}/time_series.png"),
                "alt_text": "Time Series Trends"
            },
            {
                "title": "Outlier Detection (Box Plot)",
                "description": "Box plots for each numerical variable showing the distribution, quartiles, and potential outliers. Outliers are data points that fall significantly outside the typical range (beyond 1.5 times the interquartile range). Identifying and understanding outliers is crucial for data quality assessment and model robustness.",
                "image_data": image_to_base64(f"{images_base_path}/outliers.png"),
                "alt_text": "Box Plots for Outlier Detection"
            },
            {
                "title": "Lagged Correlation Analysis (Lag = 1)",
                "description": "Correlation matrix showing relationships between variables and their lagged values (shifted by one time period). This is particularly useful in marketing mix modeling to identify delayed effects—for example, how today's marketing spend influences tomorrow's sales. A lag of 1 indicates the analysis compares each value with the previous period's value.",
                "image_data": image_to_base64(f"{images_base_path}/lag_correlation_lag1.png"),
                "alt_text": "Lag Correlation Analysis"
            }
        ],

        # Footer information
        "generator": "OwlMix EDA Module",
        "report_date": "April 10, 2026"
    }

if __name__ == "__main__":
    # File paths
    template_path = "outputs/eda_report_template.html"
    output_path = "outputs/rendered_eda_report.html"
    images_base_path = "outputs"

    # Get sample data
    data = get_sample_data(images_base_path)

    # Generate the report
    generate_eda_report(template_path, output_path, data, images_base_path)