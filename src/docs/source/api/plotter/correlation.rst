.. _correlation:

Correlation Module - Plotting
=============================

.. currentmodule:: owlmix.plotting.correlation

The ``CorrelationPlotter`` class provides functionality to visualize correlation matrices and lagged correlation matrices for tabular data. This module helps users understand the relationships between variables by generating informative heatmaps.

Overview
--------

The module exposes a plotter class that:

- Accepts correlation analysis results as input
- Plots the correlation matrix and lagged correlation matrix as heatmaps
- Supports output directory customization
- Leverages `matplotlib` and `seaborn` for visualization

Class Reference
---------------

.. autoclass:: owlmix.plotting.correlation.CorrelationPlotter
   :members:
   :show-inheritance:

   Plots the correlation matrix and lagged correlation matrix for the provided data.

   :param data: Dictionary containing correlation matrices (e.g., "correlation_matrix", "lagged_correlation_matrix").
   :type data: dict
   :param params: Configuration parameters for correlation plotting.
   :type params: CorrPlotParams

   **Example:**

   .. code-block:: python

      import pandas as pd
      from owlmix.utils.sample_data_generator import create_sample_data
      from owlmix.analysis.correlation import CorrelationAnalyzer, CorrelationParams
      from owlmix.plotting.correlation import CorrelationPlotter, CorrPlotParams

      # Generate sample data
      df = create_sample_data(n=100)

      # Define parameters for CorrelationAnalyzer
      params = CorrelationParams(
          columns=None,  # Use all numeric columns
          n_lags=25,
          precision=4
      )

      # Create and compute the analyzer
      analyzer = CorrelationAnalyzer(df, params)
      result = analyzer.compute()

      # Create and generate the plotter
      plotter = CorrelationPlotter(result)
      corr_file_path, lagged_corr_file_path = plotter.generate(output_dir="outputs/charts")

Methods
-------

.. py:method:: generate(output_dir: str = "outputs/charts") -> tuple[str, str]

   Generates and saves the correlation matrix and lagged correlation matrix heatmaps.

   :param output_dir: Directory to save the generated plots.
   :type output_dir: str
   :returns: Tuple of file paths to the saved correlation matrix and lagged correlation matrix images.

Sample Output
-------------

**Correlation Matrix** and **Lagged Correlation Matrix** plots are heatmaps where each cell represents the correlation coefficient between two variables (or variable and lag). The color intensity indicates the strength and direction of the correlation.

.. image:: /_static/image/corr_matrix.png
   :alt: Sample Correlation Matrix Plot
   :width: 1000px
   :align: center

.. image:: /_static/image/lagged_corr_matrix.png
   :alt: Sample Lagged Correlation Matrix Plot
   :width: 1000px
   :align: center