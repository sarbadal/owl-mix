.. _working_with_enums:

Working with Enums
==================

OwlMix uses **Enums** (Enumerations) to standardize configuration values. Using these instead of raw strings prevents typos and ensures your code remains compatible with future versions.

Key Enum Reference Table
^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 30 30

   * - **Enum Class**
     - **Purpose**
     - **All Available Values**
   * - ``ChartID``
     - Controlling chart visibility and order.
     - ``VIF_CHART``, ``ACF_PACF_CHART``, ``KPI_VS_FEATURE_CHART``, ``DISTRIBUTION_CHART``, ``CATEGORICAL_DISTRIBUTION_CHART``, ``CORRELATION_CHART``, ``LAG_CORRELATION_CHART``, ``TIME_SERIES_CHART``, ``OUTLIERS_CHART``, ``COMPARISON_CHART``
   * - ``Period``
     - Defining data aggregation frequency.
     - ``DAILY``, ``WEEKLY``, ``MONTHLY``, ``YEARLY``
   * - ``ComparisonType``
     - Setting logic for time-based comparisons.
     - ``YoY``, ``QoQ``, ``MoM``, ``WoW``, ``YoY_MONTH``, ``YoY_QUARTER``, ``YoY_WEEK``
   * - ``PlotMode``
     - Choosing the visual axis/unit style.
     - ``ABSOLUTE``, ``PCT_CHANGE``, ``DUAL``


Implementation Guide
^^^^^^^^^^^^^^^^^^^^

**Basic Usage**

Always import the Enum classes from ``owlmix.typing.enums``.

.. code-block:: python

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

Inspecting Enum Data
^^^^^^^^^^^^^^^^^^^^

Since all Enums inherit from ``BaseEnum``, you can programmatically inspect them if you are unsure of the underlying values or labels.

.. code-block:: python

    # Returns a list of strings: ['DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']
    print(Period.names())

    # Returns a list of raw values: ['daily', 'weekly', 'monthly', 'yearly']
    print(Period.values())

    # Returns a formatted JSON string of IDs, Names, and Labels
    print(ComparisonType.pretty_options())

.. note::

   **Pro Tip:** Use ``.label`` if you need the human-readable version for your own custom logs or UI (e.g., ``ComparisonType.YoY.label`` returns ``"Year over Year"``).