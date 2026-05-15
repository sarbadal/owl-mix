Reporting System Overview
=========================

This document provides an overview of the reporting system in the ``owlmix`` 
package, focusing on the classes and workflow for generating and rendering 
Exploratory Data Analysis (EDA) reports.

Modules Covered
---------------

- ``report_builder.py``: Defines the report data structure and orchestrates report generation.
- ``html.py``: Handles rendering of report data into HTML using Jinja2 templates.

Report Building
---------------

**Class:** ``ReportBuilder``

The ``ReportBuilder`` class is responsible for constructing a comprehensive EDA report from a pandas DataFrame. It manages the inclusion, exclusion, and ordering of report sections, and supports outputting the report as a JSON file.

**Key Attributes:**

- ``df``: The input pandas DataFrame.
- ``target_col``: The target column for analysis.
- ``date_col``: The date column for time series analysis.
- ``config``: Configuration builder for report settings.
- ``sections``: An ``OrderedDict`` mapping section names to ``SectionContent`` (data and chart).

**Key Methods:**

- ``add_section(name, data, chart=None)``: Adds a section with data and optional chart.
- ``add_section_by_name(name)``: Adds a section using a registered builder function.
- ``add_all_sections()``: Adds all registered sections.
- ``include_sections(section_names)``: Keeps only specified sections.
- ``exclude_sections(section_names)``: Removes specified sections.
- ``build(output_path=None)``: Builds the report data structure (as a dict).
- ``save(outfile_name=None)``: Saves the report as a JSON file.
- ``image_to_base64(image_path)``: Converts an image to a base64 string for embedding.

**SectionContent Dataclass:**

.. code-block:: python

    @dataclass
    class SectionContent:
        data: Dict[str, Any]
        chart: Dict[str, Any]

**Report Data Structure Example:**

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

    {
        "sections": {
            "section_name": {
                "data": { ... },
                "chart": { ... }
            },
            ...
        }
    }

HTML Rendering
--------------

**Class:** ``ReportHTMLRenderer``

The ``ReportHTMLRenderer`` class is responsible for rendering the report data (as a dictionary or JSON file) into HTML using Jinja2 templates.

**Key Attributes:**

- ``env``: Jinja2 environment for template rendering.
- ``template``: The loaded Jinja2 template (default: ``_default.html``).
- ``_html_str``: The most recently rendered HTML string.

**Key Methods:**

- ``render(report_data)``: Renders HTML from a report data dictionary.
- ``render_from_json(json_path)``: Renders HTML from a JSON file.
- ``save_html(html_str, output_path)``: Saves the rendered HTML to disk.
- ``html_str``: Property to access the last rendered HTML string.

**Typical Usage:**

.. code-block:: python

    renderer = ReportHTMLRenderer()
    html = renderer.render(report_data)
    renderer.save_html(html, output_path="outputs/report.html")

Workflow Summary
----------------

1. **Build the Report:**
   - Use ``ReportBuilder`` to add sections and build the report data structure.
   - Save the report as a JSON file if needed.

2. **Render the Report:**
   - Use ``ReportHTMLRenderer`` to render the report data (dict or JSON) into HTML.
   - Save the HTML output to disk.

3. **Customization:**
   - Custom Jinja2 templates can be provided via the ``template_path`` argument to ``ReportHTMLRenderer``.

Directory Structure
-------------------

- ``owlmix/reporting/report_builder.py``: Report building logic.
- ``owlmix/reporting/html.py``: HTML rendering logic.
- ``owlmix/reporting/_templates/``: Default Jinja2 templates.

Extensibility
-------------

- New report sections can be registered and added via the ``SECTION_BUILDERS`` registry.
- Templates can be customized for different report layouts.

``owlmix`` thus provides a modular and extensible framework for automated EDA report generation and rendering.