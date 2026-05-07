Advanced Configuration
======================

**Handling Categorical Variables**

To get the most out of your analysis, it is essential to explicitly define your categorical columns. **If these are not set, OwlMix will not generate categorical distribution charts in the final report.**

**Why This Is Important**

Explicitly defining categorical variables ensures that the OwlMix engine:

* **Generates Visualizations:** Triggers the creation of frequency and distribution charts in the HTML output.
* **Ensures Data Integrity:** Correctly interprets columns as discrete categories (e.g., ``store_id`` or ``product_code``) even if they contain numerical values.

**Usage**

Use the ``update_categorical_columns_config`` method after initializing your report object, but before calling ``.run()``.

.. code-block:: python

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

.. note::

    If you find that specific charts are missing from your HTML report, double-check that the column names in your list exactly match the headers in your DataFrame.


**Customising Report Charts (Include, Exclude, & Reorder)**

You can control exactly which visualisations appear in your report and the order in which they are displayed using the ``summary_builder`` attributes. This is useful for removing noise or prioritising the most important insights for your stakeholders.

**Chart Management Options**

* **Exclude**: Remove specific charts you don't need (e.g., removing Correlation if it's not relevant).
* **Include**: Explicitly whitelist only the charts you want to see.
* **Reorder**: Define a custom sequence for the charts in the HTML output.

**Usage**

Use the ``ChartID`` enum to specify which charts to modify. These settings must be applied to ``report.summary_builder`` before calling ``.run()``.

.. code-block:: python

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

**Key Rules**

* **Precedence**: If you set ``include_charts``, OwlMix will prioritize that list and ignore exclusions outside of it.
* **Enum Usage**: Always use the ``ChartID`` enum to reference charts to avoid string typos and ensure compatibility with future updates.


**Time based comparison table and chart**

.. warning::

    **YOY (week-level) can be tricky**
    
    - Some years have **53 weeks**, others have 52
    - ISO week numbering does not perfectly align with calendar dates
    - The same week number across years may represent slightly different date ranges
    - This can lead to **minor inconsistencies in YoY week comparisons**

**Supported Comparison Types**

* **yoy_year**
  
  - Granularity: Year
  - Comparison: Current year vs previous year

* **mom**
  
  - Granularity: Month (``YYYY-MM``)
  - Comparison: Current month vs previous month

* **wow**
  
  - Granularity: Week (week start date)
  - Comparison: Current week vs previous week

* **qoq**
  
  - Granularity: Quarter (``YYYYQX``)
  - Comparison: Current quarter vs previous quarter

* **yoy_month**
  
  - Granularity: Month
  - Comparison: Same month across years (e.g., Jan 2024 vs Jan 2023)

* **yoy_quarter**
  
  - Granularity: Quarter
  - Comparison: Same quarter across years (e.g., Q1 2024 vs Q1 2023)

* **yoy_week**
  
  - Granularity: ISO Week
  - Comparison: Same week number across years