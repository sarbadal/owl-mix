.. _quickstart:

🚀 Quickstart
=============

This guide shows how to quickly generate an EDA report using the `owlmix` package.

1. **Install dependencies** (if not already installed):

   .. code-block:: bash

      pip install -r requirements.txt

2. **Generate a report and render HTML**

   .. code-block:: python

      import warnings
      from pathlib import Path

      # Suppress user warnings for cleaner output
      warnings.simplefilter('ignore', category=UserWarning)

      # Import necessary modules from owlmix
      from owlmix.utils.sample_data_generator import create_sample_data
      from owlmix.reporting import ReportBuilder, ReportHTMLRenderer

      # Set up paths
      CURRENT_DIR = Path(__file__).parent
      OUTPUT_DIR = CURRENT_DIR / "output"
      OUTPUT_DIR.mkdir(exist_ok=True)

      # Generate sample data (you should replace this with your own dataset)
      df = create_sample_data(n=500)

      # Build the report
      report_builder = ReportBuilder(
          df=df,
          target_col="sales",
          date_col="time"
      )

      # Update configuration for ACF/PACF and VIF
      report_builder.config.update_config(
          acf_pacf={
              "columns": ["sales", "tv_spend"],
              "n_lags": 5,
              "precision": 3
          },
          vif={
              "precision": 2
          },
          correlation={
            # "columns": ["sales", "tv_spend"],
            "n_lags": 8,
            "precision": 5
        }
      )

      # Add all sections to the report
      report_builder.add_all_sections(verbose=True)

      # Build and save the report as JSON
      report = report_builder.build()
      report_builder.save(OUTPUT_DIR / "result.json")

      # Render HTML from the JSON report
      renderer = ReportHTMLRenderer()
      html_str = renderer.render_from_json(OUTPUT_DIR / "result.json")
      renderer.save_html(html_str, OUTPUT_DIR / "report.html")

3. **View the generated HTML report**  
   Open `output/report.html` in your browser to see the EDA report.

Load Config from Dict, YAML, or JSON
------------------------------------

You can also load section configuration from a Python dictionary, YAML file, or JSON file.

.. code-block:: python

   # 1) From Python dict
   config_dict = {
       "acf_pacf": {
           "columns": ["sales", "tv_spend"],
           "n_lags": 10,
           "precision": 2,
       },
       "ccf": {
           "feature_columns": ["tv_spend", "digital_spend"],
           "max_lag": 3,
       },
   }
   report_builder.config.update_config_from_dict(config_dict, strict=True)

   # 2) From YAML file
   report_builder.config.update_config_from_yaml("report_config.yaml", strict=True)

   # 3) From JSON file
   report_builder.config.update_config_from_json("report_config.json", strict=True)

Notes:

- ``strict=True`` raises an error for unknown section keys.
- The top-level config must be a dictionary.
- Each section value must also be a dictionary.

:ref:`Back to Home <home>`
