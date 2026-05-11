.. _acf-pacf:

ACF and PACF Module - Plotting
==============================

.. currentmodule:: owlmix.plotting.acf_pacf

The ``AcfPacfPlotter`` class provides functionality to visualize the Auto-Correlation Function (ACF) 
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

.. autoclass:: owlmix.plotting.acf_pacf.AcfPacfPlotter
   :members:
   :show-inheritance:

   Plots the Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF)
   for specified columns in a pandas DataFrame or a single Series.

   :param data: Input DataFrame or Series containing time series data.
   :type data: pandas.DataFrame or pandas.Series
   :param params: Configuration parameters for ACF/PACF plotting.
   :type params: AcfPacfParams

   **Example:**

   .. code-block:: python

      import pandas as pd
      from owlmix.plotting.acf_pacf import AcfPacfPlotter

      data = [
          {
             "column": "sales",
             "n_obs": 500,
             "lags": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
             "acf": [1.0, -0.0145, -0.0466, 0.0489, -0.0108, 0.0131, -0.031, 0.0764, 0.0464, -0.0455, -0.051],
             "pacf": [1.0, -0.0146, -0.047, 0.0479, -0.0118, 0.0176, -0.0346, 0.0797, 0.0446, -0.0346, -0.0586]
          }
      ]

      plotter = AcfPacfPlotter(data=data)
      plotter.plot()


Methods
-------

.. py:method:: plot()

   Generates and displays ACF and PACF plots for each specified column or series.

   :returns: None


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
