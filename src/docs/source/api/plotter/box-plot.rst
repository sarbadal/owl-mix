.. _api.plotter.box-plot:

➡️ plotting.box_plot
====================

.. currentmodule:: owlmix.plotting.box_plot

The :class:`BoxPlotter` class provides functionality to visualize the distribution 
of data using box plots. This module is designed to help users understand the spread, 
central tendency, and outliers in their data by generating informative box plot grids.

Overview
--------

The module exposes a plotter class that:

- Accepts a dictionary of statistics for each column
- Plots box plots for each column in a grid layout
- Supports configurable number of plots per row
- Leverages `matplotlib` and `numpy` for visualization

Class Reference
---------------

.. py:class:: BoxPlotParams(n_plot_per_row=4)

   Dataclass for specifying box plot grid parameters.

   :param n_plot_per_row: Number of box plots per row in the grid.
   :type n_plot_per_row: ``int``

.. py:class:: BoxPlotter(data, params=BoxPlotParams)

   Plots box plots for the provided data statistics.

   :param data: Dictionary containing statistics for each column.
   :type data: ``Dict[str, Dict[str, Any]]``
   :param params: Configuration parameters for box plot grid.
   :type params: ``BoxPlotParams``

   .. py:method:: generate(output_dir: str = "outputs/charts") -> Optional[str]

      Generates and saves a grid of box plots for the provided data.

      :param output_dir: Directory to save the generated plot image.
      :type output_dir: ``str``
      :returns: File path to the saved box plot grid image, or None if no data.
      :rtype: ``Optional[str]``

Sample Output
-------------

A box plot grid typically consists of multiple subplots, each representing the 
distribution of a column. Each box shows the median, quartiles, whiskers (min/max), 
and outliers (if any). Outliers are highlighted in red.

.. image:: /_static/image/box_plot_grid.png
   :alt: Sample Box Plot Grid
   :width: 800px
   :align: center

:ref:`Back to Home <home>`