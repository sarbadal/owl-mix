Configuration API Reference
==================================

OwlMix provides a comprehensive suite of ``update_*`` methods to fine-tune your analysis. These methods allow you to modify statistical parameters, chart aesthetics, and data processing logic.

**Implementation Pattern**

All configuration updates must be performed on the ``report.config`` object **after** initialization and **before** calling ``report.run()``.

.. code-block:: python

    report = OwlMixReport(df=df, target="sales", date_column="date")

    # Example: Chaining configuration updates
    report.config.update_categorical_columns_config(columns=["brand", "store_id"]) \
                 .update_correlation_config(method="pearson") \
                 .update_acf_pacf_config(lags=40)


**Available Update Methods & Parameters**


+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| Method                                        | Description                                                   | Parameters (Keyword Arguments)                                |
+===============================================+===============================================================+===============================================================+
| ``update_categorical_columns_config``         | **Essential:** Defines columns for categorical analysis.       | ``columns``                                                   |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_time_series_config``                 | Configures the primary time series visualization.              | ``columns``, ``model``, ``period``                           |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_time_aggregator_config``             | Controls how data is grouped and aggregated.                   | ``date_column``, ``value_columns``, ``agg_func``,            |
|                                               |                                                               | ``precision``, ``freq``                                      |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_time_comparison_config``             | Defines logic for PoP or YoY comparisons.                      | ``date_column``, ``value_columns``, ``comparison_type``,     |
|                                               |                                                               | ``agg_func``, ``precision``, ``freq``                        |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_time_comparison_chart_config``       | Adjusts the visual layout of comparison charts.                | ``date_column``, ``value_columns``, ``comparison_type``,     |
|                                               |                                                               | ``agg_func``, ``mode``                                       |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_correlation_config``                 | Sets parameters for correlation analysis.                      | ``columns``                                                  |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_correlation_chart_layout_config``    | Customizes the heatmap UI and labels.                          | ``columns``                                                  |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_lag_corr_chart_config``              | Configures cross-correlation with time lags.                   | ``column`` (required), ``lag``                               |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_acf_pacf_config``                    | Adjusts lags and markers for ACF/PACF plots.                   | ``columns``, ``n_lags``, ``acf_marker``, ``pacf_marker``,    |
|                                               |                                                               | ``acf_stem``, ``pacf_stem``, ``acf_conf``, ``pacf_conf``     |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_distribution_chart_config``          | Sets binning logic and chart grid layout.                      | ``columns``, ``max_charts_per_row``                          |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_kpi_vs_feature_config``              | Configures analysis of Target vs Features.                     | ``target_column``, ``columns``, ``period``,                  |
|                                               |                                                               | ``date_column``, ``agg_func``                                |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_causality_test_config``              | Fine-tunes Granger causality test parameters.                  | ``target_column``, ``columns``, ``max_lag``,                 |
|                                               |                                                               | ``error_threshold``, ``p_value_weight``, ``mape_weight``     |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_vif_config``                         | Configures multicollinearity detection.                        | ``target_column``, ``features``, ``precision``,              |
|                                               |                                                               | ``color_thresholds``                                         |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+
| ``update_outlier_chart_layout_config``        | Adjusts outlier detection and visual markers.                  | ``columns``, ``max_cols_per_chart``, ``single_image``        |
+-----------------------------------------------+---------------------------------------------------------------+---------------------------------------------------------------+

**Quick Usage Tip**


When passing values to these methods, ensure you use the argument names exactly as listed. For example:

.. code-block:: python

    report.config.update_vif_config(
        features=["price", "inventory", "promotion"],
        precision=2
    )

**Pro-Tips**

* **Method Chaining:** These methods return ``self``, so you can chain multiple updates together for cleaner code.
* **Validation:** If a chart is missing from your report, verify that its corresponding ``update_`` method has been called with the correct column names.
* **Enums:** For methods like ``update_correlation_config``, it is recommended to use the built-in ``owlmix.typing.enums`` to ensure parameter validity.


**Custom VIF Color Thresholds**

The Variance Inflation Factor (VIF) is used to detect multicollinearity among features. To make the report more intuitive, OwlMix allows you to define **Rule-Based Coloring**. This feature applies specific colors to VIF bars based on their numerical value.

**Why Customize Thresholds?**

Different industries have different tolerances for multicollinearity. While a VIF of 5 is often considered "high," some models require stricter thresholds (e.g., 2.5) or allow for more leniency. Custom colors help stakeholders instantly identify "Safe," "Warning," or "Critical" variables.

**Usage**

You can pass a list of tuples to the ``color_thresholds`` parameter within ``update_vif_config``. Each tuple should follow the format: ``(upper_bound, "color_name_or_hex")``.

.. code-block:: python

    # 1. Define your rules (value, color)
    # The rule applies if the VIF value is less than or equal to the threshold
    vif_color_rules = [
        (2, "blue"),              # Safe: VIF <= 2
        (5, "green"),             # Moderate: 2 < VIF <= 5
        (6, "yellow"),            # Warning: 5 < VIF <= 6
        (10, "red"),              # High: 6 < VIF <= 10
        (float("inf"), "darkred") # Critical: VIF > 10
    ]

    # 2. Update the VIF configuration
    report.config.update_vif_config(color_thresholds=vif_color_rules)

    # 3. Run the report
    report.run(html_file_name="vif_analysis.html")

**Key Rules**

* **Order Matters**: List your thresholds in **ascending order**. OwlMix evaluates these rules sequentially.
* **Infinity**: Use ``float("inf")`` as the final threshold to catch all values exceeding your last defined limit.
* **Color Support**: You can use standard CSS color names (e.g., ``"red"``, ``"orange"``) or Hex codes (e.g., ``"#FF5733"``).

.. note::

    **Default Behavior:** If no custom thresholds are provided, OwlMix uses a standard internal color palette to differentiate VIF levels.