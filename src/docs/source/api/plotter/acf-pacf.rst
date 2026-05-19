.. _api.plotter.acf-pacf:

✎ᝰ plotting.acf_pacf
=====================

.. currentmodule:: owlmix.plotting.acf_pacf

The :class:`AcfPacfPlotter` class provides functionality to visualize the Auto-Correlation Function (ACF) 
and Partial Auto-Correlation Function (PACF) for time series data. This module is designed to 
help users understand the correlation structure of their time series data by generating informative plots.

Overview
--------

The module exposes a plotter class that:

- Accepts a pandas DataFrame or Series
- Plots ACF and PACF for selected columns or series
- Supports configurable lag values and plot customization
- Leverages `matplotlib` and `statsmodels` for visualization

Class Reference
---------------

.. py:class:: AcfPacfPlotParams(columns=None, n_lags=10, precision=4)

   Dataclass for specifying ACF/PACF plotting parameters.

.. py:class:: AcfPacfPlotter(data, params)

   Plots the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF)
   for specified columns in a pandas DataFrame or a single Series.

   :param data: Input DataFrame or Series containing time series data.
   :type data: ``pandas.DataFrame`` or ``pandas.Series``
   :param params: Configuration parameters for ACF/PACF plotting.
   :type params: ``AcfPacfPlotParams``

   .. py:method:: generate(output_dir: str = "outputs/charts") -> str

      Generates and saves ACF and PACF plots for each specified column or series.

      :param output_dir: Directory to save the generated plots.
      :type output_dir: ``str``
      :returns: File path to the saved ACF and PACF chart image.
      :rtype: ``str``


Sample Output
-------------

**ACF** and **PACF** plot typically consists of two subplots: the upper subplot shows the ACF values for each lag, 
while the lower subplot shows the PACF values. Each bar represents the correlation at a specific lag, 
and horizontal lines indicate confidence intervals. Significant correlations outside these intervals 
suggest potential patterns in the time series data.

.. image:: /_static/image/acf_pacf.png
   :alt: Sample ACF and PACF Plot
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