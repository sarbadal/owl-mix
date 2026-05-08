Dual Axis Line Chart Data Generator
==================================

.. currentmodule:: owlmix.eda.kpi_vs_feature

Overview
--------

The ``DualAxisLineChartDataGenerator`` class generates data for dual-axis line charts, allowing users to compare a Key Performance Indicator (KPI) against multiple features over time. This is useful for visualizing trends and relationships between a target metric and other variables in your dataset.

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

See Also
--------

- :class:`owlmix.eda.kpi_vs_feature.DualAxisLineChartDataGenerator` for generating data for dual-axis line charts.
