.. _quickstart:

Quick Start
===========

.. code-block:: python

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

**Output:**

- ``eda_report.json``: Structured analysis data in JSON format
- ``eda_report.html``: Interactive HTML report with charts and statistics
- ``outputs/charts/``: Generated visualization files