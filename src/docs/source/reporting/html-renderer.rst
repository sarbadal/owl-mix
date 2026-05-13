Report HTML Renderer
====================

.. module:: html
   :synopsis: Provides the ReportHTMLRenderer class for rendering HTML reports from data using Jinja2 templates.

Overview
--------

This module provides the :class:`ReportHTMLRenderer` class for rendering HTML reports from structured data using Jinja2 templates. 
It supports rendering from both Python dictionaries and JSON files, and saving the resulting HTML to disk.

Key Features
~~~~~~~~~~~~

- Configurable template path for custom report layouts
- Rendering from in-memory data or JSON files
- Safe file output with directory creation

Typical usage example::

    renderer = ReportHTMLRenderer()
    html = renderer.render(report_data)
    renderer.save_html(html, output_path="outputs/report.html")

Classes
-------

ReportHTMLRenderer
~~~~~~~~~~~~~~~~~

.. class:: ReportHTMLRenderer(template_path: str | Path = DEFAULT_TEMPLATE_PATH)

   Renders HTML reports from structured data using Jinja2 templates.

   This class provides methods to render HTML from a Python dictionary or a JSON file,
   and to save the rendered HTML to disk. It is designed for use in automated EDA or analytics
   pipelines where reports need to be generated programmatically.

   :param template_path: Path to the directory containing Jinja2 templates. Defaults to the internal '_templates' directory.

   **Attributes**

   .. attribute:: env

      The Jinja2 environment for template rendering.

   .. attribute:: template

      The loaded Jinja2 template used for rendering.

   .. attribute:: _html_str

      The most recently rendered HTML string, or None if not rendered yet.

   **Methods**

   .. method:: render(report_data: dict) -> str

      Render HTML from a dictionary of report data.

      :param report_data: The report data to render. Should contain a "sections" key with section data.
      :type report_data: dict
      :returns: The rendered HTML as a string.
      :rtype: str

   .. method:: render_from_json(json_path: str | Path) -> str

      Render HTML from a JSON file containing report data.

      :param json_path: Path to the JSON file with report data.
      :type json_path: str or Path
      :returns: The rendered HTML as a string.
      :rtype: str

   .. method:: save_html(html_str: str = None, output_path: str | Path = None)

      Save the rendered HTML to a file.

      :param html_str: The HTML string to save. If None, uses the last rendered HTML.
      :type html_str: str, optional
      :param output_path: The file path to save the HTML to.
      :type output_path: str or Path, optional
      :raises ValueError: If no HTML has been rendered or output_path is not specified.

   .. attribute:: html_str

      Get the most recently rendered HTML string.

      :returns: The last rendered HTML string, or None if not rendered yet.
      :rtype: str or None

Module Attributes
-----------------

.. data:: DEFAULT_TEMPLATE_PATH

   Default path to the internal '_templates' directory for Jinja2 templates.

.. data:: STATIC_PATH

   Path to the internal '_static' directory for Jinja2 static assets used in reports.
