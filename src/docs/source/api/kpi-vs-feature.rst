.. _kpi-vs-feature:

Dual Axis Line Chart Data Generator
===================================

Dual axis analysis helps visualize the relationship between a KPI and one or
more feature variables over time, even when they are on different scales.
 
This is particularly useful in Market Mix Modeling (MMM), where analysts need
to quickly assess how different marketing inputs behave relative to a target KPI.
 
Why Dual Axis Analysis?
-----------------------
 
In real-world datasets:
 
- KPIs and feature variables often have different units and scales
- Direct comparison using a single axis can be misleading
- Visual alignment is more important than absolute magnitude


Dual axis charts solve this by:
 
- Plotting the KPI on one axis
- Plotting a feature variable on another axis
- Allowing visual comparison of trends and movements
 
What Insights It Provides
-------------------------
 
Using dual axis analysis, you can:
 
- Identify features that visually track or mimic the KPI
- Detect leading or lagging relationships
- Spot seasonal patterns across variables
- Quickly shortlist important variables for modeling
 
How It Works
------------
 
The system generates chart-ready data by:
 
1. Selecting a KPI column
2. Selecting one or more feature variables
3. Aggregating data over a chosen time granularity:
   - Year
   - Quarter
   - Month
   - Week
   - Day
 
For each feature variable, a separate comparison is created:
 
- KPI vs Feature 1
- KPI vs Feature 2
- ...
 
Each comparison can then be plotted as a dual-axis line chart.
 
Example Scenario
----------------
 
Suppose you are analyzing sales performance:
 
- KPI: ``sales``
- Features: ``tv_spend``, ``digital_spend``
 
Dual axis charts allow you to visually inspect:
 
- Whether TV spend aligns with sales trends
- Whether digital campaigns show stronger correlation
- Which channel responds faster or more consistently
 
When to Use
-----------
 
Use dual axis analysis when:
 
- Comparing KPI with multiple features
- Units differ significantly between variables
- You want quick visual screening before statistical analysis
- Exploring potential relationships in time series data

.. currentmodule:: owlmix.eda.kpi_vs_feature

Class Reference
---------------

.. autoclass:: DualAxisLineChartDataGenerator
   :members:
   :undoc-members:
   :show-inheritance:

Initialization
--------------

.. py:class:: DualAxisLineChartDataGenerator(df, date_column, target_column, period='monthly', columns=None, agg_func='sum')

   :param df: The input pandas DataFrame containing your data.
   :type df: pandas.DataFrame

   :param date_column: The name of the column containing date information.
   :type date_column: str

   :param target_column: The name of the KPI column to plot on the chart.
   :type target_column: str

   :param period: The period for grouping the data. Options are ``'daily'``, ``'weekly'``, ``'monthly'``, or ``'yearly'``. Default is ``'monthly'``.
   :type period: str

   :param columns: A list of feature column names to compare against the KPI. If None, all columns except the target are used.
   :type columns: list[str] or None

   :param agg_func: The aggregation function to use (e.g., ``'sum'``, ``'mean'``, ``'max'``). Default is ``'sum'``.
   :type agg_func: str

Usage Example
-------------

.. code-block:: python

   import pandas as pd
   from owlmix.eda.kpi_vs_feature import DualAxisLineChartDataGenerator

   # Example DataFrame
   df = pd.DataFrame({
       'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
       'sales': [100, 150, 200],
       'feature1': [10, 20, 30],
       'feature2': [5, 7, 9]
   })

   generator = DualAxisLineChartDataGenerator(
       df=df,
       date_column='date',
       target_column='sales',
       period='daily',
       columns=['feature1', 'feature2'],
       agg_func='sum'
   )

   chart_data = generator.generate()
   print(chart_data)

Methods
-------

.. py:method:: generate()

   Generates the structured data for dual-axis line charts.

   :returns: A dictionary with the following structure:

      .. code-block:: javascript

         {
             "data": [
                 {
                     "kpi": "sales",
                     "column": "feature1",
                     "x": ["2024-01-01", "2024-01-02", ...],
                     "target": [100, 150, ...],
                     "feature": [10, 20, ...]
                 },
                 {
                     "kpi": "sales",
                     "column": "feature2",
                     "x": ["2024-01-01", "2024-01-02", ...],
                     "target": [100, 150, ...],
                     "feature": [5, 7, ...]
                 }
             ]
         }

   Each entry in the ``data`` list corresponds to a feature column compared against the KPI.

Details
-------

- **Date Handling:** The class automatically converts the date column to datetime and groups data by the specified period (daily, weekly, monthly, yearly).
- **Aggregation:** The specified aggregation function is applied to both the KPI and feature columns.
- **Output:** The output is suitable for feeding into charting libraries for dual-axis line charts.


Notes
-----

- Visual similarity does not imply causation
- Always validate findings with statistical methods (e.g., correlation, causality tests)
- Time aggregation level can significantly affect interpretation
