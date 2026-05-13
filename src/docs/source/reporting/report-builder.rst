Report Builder
==============

This module defines the ``ReportBuilder`` class, which orchestrates the generation of
Exploratory Data Analysis (EDA) reports, including both textual and chart-based sections.
It provides a flexible API to add, include, exclude, and reorder report sections and charts,
and to output the report as a JSON file.

Classes and Data Structures
---------------------------

SectionContent
~~~~~~~~~~~~~

.. py:class:: SectionContent

   Data class to represent the content of a report section.

   :param data: The data associated with the section, which can include analysis results, metrics, etc.
   :type data: Dict[str, Any]
   :param chart: The chart information for the section, which can include the chart type, data for plotting, and any relevant metadata.
   :type chart: Dict[str, Any]

   .. code-block:: python

      @dataclass
      class SectionContent:
          data: Dict[str, Any]
          chart: Dict[str, Any]

ReportBuilder
~~~~~~~~~~~~~

.. py:class:: ReportBuilder(df: pd.DataFrame, target_col: str, date_col: str, config: ConfigBuilder = ConfigBuilder)

   Class to build a comprehensive EDA report with multiple sections, including both textual data and charts.

   :param df: The input DataFrame containing the data to be analyzed.
   :type df: pd.DataFrame
   :param target_col: The name of the target column in the DataFrame for analysis.
   :type target_col: str
   :param date_col: The name of the date column in the DataFrame for time series analysis.
   :type date_col: str
   :param config: An instance of ConfigBuilder to manage configuration settings for the report.
   :type config: ConfigBuilder

   **Attributes:**

   - **sections** (OrderedDict[str, SectionContent]): Stores the sections of the report, where keys are section names and values are SectionContent instances.
   - **_report_data** (Optional[Dict[str, Any]]): Cached report data after building.

   **Methods:**

   .. py:method:: add_section(name: str, data: Dict[str, Any], chart: Optional[Dict[str, Any]] = None) -> Self

      Adds a section to the report with the given name, data, and optional chart information.

      :param name: The name of the section to add.
      :param data: The data associated with the section.
      :param chart: The chart information for the section (optional).
      :return: The current instance of the ReportBuilder.

   .. py:method:: add_section_by_name(name: str) -> Self

      Adds a section to the report by looking up a registered section builder function by name and executing it.

      :param name: The name of the section to add.
      :return: The current instance of the ReportBuilder.
      :raises ValueError: If no section builder is registered for the given name.

   .. py:method:: add_all_sections(verbose: bool = False) -> None

      Adds all registered sections to the report by iterating through the SECTION_BUILDERS registry and adding each section by name.
      
      :param verbose: If True, prints the name of each section as it is added to the report. Default is False.

   .. py:method:: include_sections(section_names: list[Union[str, SectionEnum]]) -> None

      Keep only the specified sections in the report.

      :param section_names: List of section names or SectionEnum members to include.

   .. py:method:: exclude_sections(section_names: list[Union[str, SectionEnum]]) -> None

      Excludes specified sections from the report by removing them from the sections dictionary.

      :param section_names: List of section names or SectionEnum members to be excluded from the report.

   .. py:method:: build(output_path: Optional[str] = None) -> Dict[str, Any]

      Builds the report data structure, which can be output as JSON or used for further processing.

      :param output_path: The path where the report should be saved as a JSON file. If None, the report is not saved to a file.
      :return: A dictionary representing the report data, including sections and their associated data and charts.

      **Example Output:**

      .. code-block:: javascript

         {
             "sections": {
                 "section_name": {
                     "data": { ... },
                     "chart": { ... }
                 },
                 ...
             }
         }

   .. py:method:: image_to_base64(image_path: str) -> str

      Convert an image file to a base64 string for embedding in HTML.

      :param image_path: Path to the image file.
      :return: Base64-encoded image string with MIME type, or empty string if not found.

   .. py:method:: save(outfile_name: Optional[str] = None) -> None

      Save the generated report as a JSON file.

      :param outfile_name: The name of the output JSON file. If None, defaults to "report.json".

Usage Example
-------------

.. code-block:: python

   import pandas as pd
   from owlmix.reporting.report_builder import ReportBuilder

   df = pd.read_csv("data.csv")
   builder = ReportBuilder(df, target_col="target", date_col="date")
   builder.add_all_sections()
   builder.save("my_report.json")

Design Notes
------------

- Sections are registered via the ``SECTION_BUILDERS`` registry and can be added by name.
- The report structure is designed for easy serialization to JSON and further rendering (e.g., to HTML).
- Images can be embedded in the report as base64 strings for portability.

Dependencies
------------

- pandas
- base64
- json
- dataclasses
- collections
- typing
- ConfigBuilder from owlmix.config.config_builder
