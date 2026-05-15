.. _correlation:

plotting.correlation
====================

.. currentmodule:: owlmix.plotting.correlation

The :class:`CorrelationPlotter` class provides functionality to visualize correlation matrices and lagged correlation matrices for tabular data. This module helps users understand the relationships between variables by generating informative heatmaps.

Overview
--------

The module exposes a plotter class that:

- Accepts correlation analysis results as input
- Plots the correlation matrix and lagged correlation matrix as heatmaps
- Supports output directory customization
- Leverages `matplotlib` and `seaborn` for visualization

Class Reference
---------------

.. py:class:: CorrPlotParams

   Dataclass for specifying correlation plotting parameters.

.. py:class:: CorrelationPlotter(data, params)

   Plots the correlation matrix and lagged correlation matrix for the provided data.

   :param data: Dictionary containing correlation matrices (e.g., "correlation_matrix", "lagged_correlation_matrix").
   :type data: ``dict``
   :param params: Configuration parameters for correlation plotting.
   :type params: ``CorrPlotParams``

   .. py:method:: generate(output_dir: str = "outputs/charts") -> tuple[str, str]

      Generates and saves the correlation matrix and lagged correlation matrix heatmaps.

      :param output_dir: Directory to save the generated plots.
      :type output_dir: ``str``
      :returns: Tuple of file paths to the saved correlation matrix and lagged correlation matrix images.
      :rtype: ``tuple[str, str]``


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