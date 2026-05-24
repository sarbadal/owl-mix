.. _home:

Welcome to OwlMix's documentation!
==================================
 
OwlMix is a Python library for performing advanced exploratory data analysis (EDA),
including lag analysis, correlation insights, and automated reporting.
 
✨ Key Features
---------------
 
- Automated EDA report generation
- Time series lag analysis
- Correlation and statistical insights
- Easy-to-use API for quick integration
 
🚀 Quick Example
----------------
 
.. code-block:: python
 
   import pandas as pd
   from owlmix.report import OwlMixReport

   # Load your data
   df = pd.read_csv("your_data.csv")

   # Create and generate report
   report = OwlMixReport(
      df=df,
      target="kpi",                             # Target variable for analysis
      date_column="date",                       # Date column for time series analysis
      template_name="custom_eda_template.html"  # Optional: use "custom_eda_template_dark.html" for dark theme
   )

   # Generate HTML and JSON reports
   report.run(
      json_file_name="eda_report.json",
      html_file_name="eda_report.html"
   )
 
📚 Documentation Overview
-------------------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :hidden:
 
   getting-started/quickstart
   getting-started/installation

🚀 Get Started
--------------

:doc:`Quick Start Guide <getting-started/quickstart>`

A step-by-step guide to quickly get up and running with OwlMix.

:doc:`Installation Instructions <getting-started/installation>`

Detailed instructions for installing OwlMix.


.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :hidden:
 
   user-guide/overview

📖 User Guide
-------------

:doc:`User Guide Overview <user-guide/overview>`

This section provides a comprehensive user guide for OwlMix, covering the main 
features, configuration options, and best practices for using the library 
effectively in your data analysis workflow.

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   :hidden:

   api/overview
   api/analysis/acf-pacf
   api/analysis/box-plot
   api/analysis/causality
   api/analysis/ccf
   api/analysis/correlation
   api/analysis/vif
   api/plotter/acf-pacf
   api/plotter/box-plot
   api/plotter/dual-axis-line
   api/plotter/correlation
   api/plotter/vif
   api/utils/file-resolver

🧾 API Reference
----------------

:doc:`API Overview <api/overview>`

This section provides an overview of the API documentation for the ``owlmix`` package, 
focusing on the main analytical, plotting, utility, and typing modules.

**Analysis Modules** 

- :doc:`ACF/PACF Analysis <api/analysis/acf-pacf>` Documentation for the ACF/PACF analysis module, including the main classes, functions, and usage examples.
- :doc:`Box Plot Analysis <api/analysis/box-plot>` Documentation for the box plot analysis module, including the main classes, functions, and usage examples.
- :doc:`Causality Analysis <api/analysis/causality>` Documentation for the causality analysis module, including the main classes, functions, and usage examples.
- :doc:`CCF Analysis <api/analysis/ccf>` Documentation for the CCF analysis module, including the main classes, functions, and usage examples.
- :doc:`Correlation Analysis <api/analysis/correlation>` Documentation for the correlation analysis module, including the main classes, functions, and usage examples.
- :doc:`VIF Analysis <api/analysis/vif>` Documentation for the VIF analysis module, including the main classes, functions, and usage examples.

**Plotter Modules** 

- :doc:`ACF/PACF Plotting <api/plotter/acf-pacf>` Documentation for the ACF/PACF plotting module, including the main classes, functions, and usage examples.
- :doc:`Box Plot Plotting <api/plotter/box-plot>` Documentation for the box plot plotting module, including the main classes, functions, and usage examples.
- :doc:`Dual Axis Line Plotting <api/plotter/dual-axis-line>` Documentation for the dual axis line plotting module, including the main classes, functions, and usage examples.
- :doc:`Correlation Plotting <api/plotter/correlation>` Documentation for the correlation plotting module, including the main classes, functions, and usage examples.
- :doc:`VIF Plotting <api/plotter/vif>` Documentation for the VIF plotting module, including the main classes, functions, and usage examples.

.. toctree::
   :maxdepth: 2
   :caption: Reporting
   :hidden:

   reporting/overview
   reporting/html-renderer
   reporting/report-builder
   reporting/section/acf-pacf
   reporting/section/box-plot
   reporting/section/causality
   reporting/section/ccf
   reporting/section/correlation
   reporting/section/vif
   reporting/section/protocol-cls

🧾 MMM Module Overview
---------------------------------------------------------------------

- :doc:`Overview <mmm/overview>`
- :doc:`Configuration Overview <mmm/config/overview>`
- :doc:`Analysis Overview <mmm/analysis/overview>`

The MMM (Marketing Mix Modeling) module provides tools and utilities for building, 
analyzing, and visualizing marketing mix models. It includes various submodules 
for configuration, analysis, modeling, data transformation, and visualization.

.. toctree::
   :maxdepth: 2
   :caption: MMM Module
   :hidden:

   mmm/overview
   mmm/config/overview
   mmm/analysis/overview
   mmm/analysis/classifier
   mmm/analysis/contribution

📁 Reporting Sections
---------------------

:doc:`Reporting Sections <reporting/overview>` 

This section provides detailed documentation on the individual sections that 
can be included in the generated reports, such as ACF/PACF analysis, 
causality analysis, correlation analysis, CCF analysis, VIF analysis, and box plots. 
Each section is implemented as a function that integrates with the report 
builder framework and utilizes registered analyzers and plotters to 
compute and visualize insights from the data.

:doc:`Reporting Protocols <reporting/section/protocol-cls>`

This section documents the protocol classes used in the reporting framework, 
including the `ReportBuilderProtocol` which defines the interface for report 
builders, and the `SectionProtocol` which defines the interface 
for individual report sections.

:doc:`Report Builder <reporting/report-builder>`

This section provides documentation on the `ReportBuilder` class, which is 
responsible for orchestrating the construction of the report by managing the 
DataFrame, configuration, and registered sections. It provides methods for adding 
sections, retrieving configuration, and building the final report.

:doc:`HTML Renderer <reporting/html-renderer>`

This section documents the `HTMLRenderer` class, which is responsible for rendering 
the final report as an HTML file. It takes the computed data and chart metadata 
from the report builder and generates an HTML report using a specified template, 
embedding the charts and insights in a visually appealing manner.

**Additional Resources:**

- :doc:`ACF/PACF Section <reporting/section/acf-pacf>`
- :doc:`Box Plot Section <reporting/section/box-plot>`
- :doc:`Causality Section <reporting/section/causality>`
- :doc:`CCF Section <reporting/section/ccf>`
- :doc:`Correlation Section <reporting/section/correlation>`
- :doc:`VIF Section <reporting/section/vif>`
- :doc:`Protocol Classes <reporting/section/protocol-cls>`

.. toctree::
   :maxdepth: 2
   :caption: Type Definitions
   :hidden:

   api/typing

❛ ❜ Type Annotations and Conventions
------------------------------------

:doc:`Type Annotations and Conventions <api/typing>`

This section documents the type annotations, custom types, and conventions used 
across the package to ensure code clarity and type safety.


.. toctree::
   :maxdepth: 2
   :caption: Examples
   :hidden:

   examples/example-eda

Examples
--------

Here you can find the example html report generated from the EDA example in the documentation.

:doc:`Example: Exploratory Data Analysis <examples/example-eda>`

`Open Example <_static/report/>`_

Contributing
------------

:doc:`Contribution Overview <contribution/overview>`

This section provides guidelines and instructions for contributing to the OwlMix 
project, including how to report bugs, suggest features, and submit code 
contributions through GitHub Issues and Pull Requests. It also outlines the contribution 
workflow and best practices for ensuring that contributions are effective 
and aligned with the project's goals.

.. toctree::
   :maxdepth: 2
   :caption: Contribution
   :hidden:

   contribution/overview
