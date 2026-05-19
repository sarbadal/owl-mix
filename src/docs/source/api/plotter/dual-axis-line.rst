.. _api.plotter.dual-axis-line:

✎ᝰ plotting.dual_axis_line
===========================

.. currentmodule:: owlmix.plotting.dual_axis_line

The :class:`DualAxisLinePreparer` class and its associated configuration dataclass 
provide functionality to prepare and transform time series data for dual-axis 
line plotting. This module is designed to help users visualize and compare two 
series (typically a KPI and a feature) over time, with options for smoothing, 
normalization, and transformation.

Overview
--------

This module exposes:

- A configuration dataclass for specifying time, target, and feature columns, as well as smoothing and normalization options.
- A preparer class that:

  - Sorts and cleans time series data
  - Applies optional transformations (adstock, difference, lag)
  - Resamples data to reduce the number of points for visualization
  - Smooths and normalizes series for better comparison
  - Generates output suitable for plotting, including SVG point strings

Class Reference
---------------

.. py:class:: DualAxisLineDataConfig(time_column, target_column, feature_column, smoothing_method="rolling", window=3, normalize=True)

   Dataclass for specifying dual axis line plot configuration.

   :param time_column: Name of the time column in the DataFrame.
   :type time_column: ``str``
   :param target_column: Name of the KPI/target column.
   :type target_column: ``str``
   :param feature_column: Name of the feature column to compare.
   :type feature_column: ``str``
   :param smoothing_method: Smoothing method to use ("rolling", "ema", or None).
   :type smoothing_method: ``str``
   :param window: Window size for smoothing.
   :type window: ``int``
   :param normalize: Whether to normalize the series to [0, 1].
   :type normalize: ``bool``

.. py:class:: DualAxisLinePreparer(df, config)

   Prepares time series data for dual axis line plotting.

   :param df: Input DataFrame containing time, target, and feature columns.
   :type df: ``pandas.DataFrame``
   :param config: Configuration parameters for the plot.
   :type config: ``DualAxisLineDataConfig``

   .. py:method:: apply_transformation(transformer_name: str, lag: int = 0) -> Self

      Applies a transformation (adstock, difference, lag) to the feature column.

      :param transformer_name: Name of the transformer ("adstock", "difference", "lag").
      :type transformer_name: ``str``
      :param lag: Lag value for lag transformation.
      :type lag: ``int``
      :returns: Self for method chaining.
      :rtype: ``DualAxisLinePreparer``

   .. py:method:: prepare(width: int = 300, height: int = 80, left_pad: int = 30, top_pad: int = 10) -> Dict[str, Any]

      Prepares the data for plotting, applying sorting, cleaning, resampling, smoothing, normalization, and output formatting.

      :param width: Width of the plot area (for SVG point calculation).
      :type width: ``int``
      :param height: Height of the plot area.
      :type height: ``int``
      :param left_pad: Left padding for the plot.
      :type left_pad: ``int``
      :param top_pad: Top padding for the plot.
      :type top_pad: ``int``
      :returns: Dictionary containing time, KPI, and feature series (raw, smoothed, normalized, min/max, SVG points).
      :rtype: ``Dict[str, Any]``

Details
-------

The output dictionary from :meth:`prepare` contains:

- ``time``: List of time values as strings
- ``kpi``: Dictionary with keys ``raw``, ``smooth``, ``normalized``, ``min``, ``max``, ``points``
- ``feature``: Dictionary with keys ``raw``, ``smooth``, ``normalized``, ``min``, ``max``, ``points``

Each ``points`` value is a string of SVG coordinates for plotting the normalized series.

Transformations
---------------

The following transformations are supported for the feature column:

- **Adstock**: Applies adstock transformation with configurable decay.
- **Difference**: Computes the difference over a specified period.
- **Lag**: Shifts the series by a specified lag.

Smoothing Methods
-----------------

- **Rolling**: Moving average with a configurable window.
- **EMA**: Exponential moving average.
- **None**: No smoothing.

Sample Output
-------------
The prepared data can be used to create a dual-axis line plot where the KPI and 
feature series are plotted on the same time axis but with different y-axes. 
The smoothed and normalized series allow for better visual comparison, 
while the raw series can be used for reference.

.. image:: /_static/image/dual_axis_line.png
   :alt: Sample Dual Axis Line Plot
   :width: 800px
   :align: center

References
----------

- :ref:`ACF and PACF Analysis <api.analysis.acf-pacf>`
- :ref:`Box Plot Analysis <api.analysis.box-plot>`
- :ref:`Causality Analysis <api.analysis.causality>`
- :ref:`Cross-Correlation Function Analysis <api.analysis.ccf>`
- :ref:`Correlation Analysis <api.analysis.correlation>`
- :ref:`Variance Inflation Factor Analysis <api.analysis.vif>`
- :ref:`ACF and PACF Plotting <api.plotter.acf-pacf>`
- :ref:`Box Plotting <api.plotter.box-plot>`
- :ref:`Correlation Heatmap Plotting <api.plotter.correlation>`
- :ref:`Variance Inflation Factor Plotting <api.plotter.vif>`
- :ref:`Dual Axis Line Plotting <api.plotter.dual-axis-line>`

:ref:`Back to Home <home>`