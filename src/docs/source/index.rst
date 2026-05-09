Welcome to OwlMix's documentation!
=======================================
 
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
 
   getting-started/installation
   getting-started/quickstart


.. toctree::
   :maxdepth: 2
   :caption: User Guide
 
   user-guide/overview


.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/acf-pacf
   api/kpi-vs-feature
