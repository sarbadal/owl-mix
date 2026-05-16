.. _api.overview:

API Overview
============

This document provides an overview of the API documentation for the ``owlmix`` package, 
focusing on the main analytical, plotting, utility, and typing modules.

Modules Covered
---------------

- ``analysis/``: Analytical methods and statistical tools for EDA.
- ``plotter/``: Plotting utilities for visualizing analysis results.
- ``utils/``: Utility functions for file operations and support tasks.
- ``typing.rst``: Type definitions and conventions.

Analysis Modules
----------------

The ``analysis`` subpackage provides core analytical tools for exploratory data analysis:

- :ref:`ACF/PACF <api.analysis.acf-pacf>`: Autocorrelation and partial autocorrelation analysis.
- :ref:`Box Plot <api.analysis.box-plot>`: Box plot statistics and visualization.
- :ref:`Causality <api.analysis.causality>`: Methods for causal inference and analysis.
- :ref:`Correlation <api.analysis.correlation>`: Correlation metrics and computation.
- :ref:`VIF <api.analysis.vif>`: Variance Inflation Factor (VIF) analysis for multicollinearity.

Each module documents the main classes, functions, and usage examples for its respective analysis.

Plotter Modules
---------------

The ``plotter`` subpackage contains plotting utilities for visualizing the results of analytical methods:

- :ref:`ACF/PACF <api.plotter.acf-pacf>`: Plotting autocorrelation and partial autocorrelation functions.
- :ref:`Box Plot <api.plotter.box-plot>`: Generating box plots for data distributions.
- :ref:`Correlation <api.plotter.correlation>`: Visualizing correlation matrices and relationships.
- :ref:`VIF <api.plotter.vif>`: Plotting VIF results for feature selection.

These modules describe the plotting APIs, input requirements, and customization options.

Utility Modules
---------------

The ``utils`` subpackage provides supporting utilities:

- :ref:`File Resolver <api.utils.file-resolver>`: Functions for resolving file paths and managing file I/O.

Directory Structure
-------------------

- ``analysis/``: Analytical methods and statistics.
- ``plotter/``: Plotting and visualization utilities.
- ``utils/``: Supporting utility functions.

Extensibility
-------------

The API is designed to be modular and extensible. New analytical or plotting 
modules can be added as needed, and utility functions can be extended to 
support additional workflows.

Summary
-------

The API documentation provides detailed reference material for the analytical, 
plotting, and utility components of the ``owlmix`` package, supporting robust 
and extensible exploratory data analysis workflows.

:ref:`Back to Home <home>`