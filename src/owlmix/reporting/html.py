"""
html.py
--------

This module provides the ReportHTMLRenderer class for rendering HTML reports from data using Jinja2 templates.
It supports rendering from both Python dictionaries and JSON files, and saving the resulting HTML to disk.

Key Features:
- Configurable template path for custom report layouts
- Rendering from in-memory data or JSON files
- Safe file output with directory creation

Typical usage example:
    renderer = ReportHTMLRenderer()
    html = renderer.render(report_data)
    renderer.save_html(html, output_path="outputs/report.html")
"""

import os
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

DEFAULT_TEMPLATE_PATH = Path(__file__).parent / "_templates"

class ReportHTMLRenderer:
    """
    Renders HTML reports from structured data using Jinja2 templates.

    This class provides methods to render HTML from a Python dictionary or a JSON file,
    and to save the rendered HTML to disk. It is designed for use in automated EDA or analytics
    pipelines where reports need to be generated programmatically.

    Args:
        template_path (str | Path, optional): Path to the directory containing Jinja2 templates.
            Defaults to the internal '_templates' directory.

    Attributes:
        env (jinja2.Environment): The Jinja2 environment for template rendering.
        template (jinja2.Template): The loaded Jinja2 template used for rendering.
        _html_str (str | None): The most recently rendered HTML string, or None if not rendered yet.

    Methods:
        render(report_data): Render HTML from a dictionary of report data.
        render_from_json(json_path): Render HTML from a JSON file containing report data.
        save_html(html_str, output_path): Save the rendered HTML to a file.
        html_str: Property to access the last rendered HTML string.
    """
    def __init__(self, template_path: str | Path = DEFAULT_TEMPLATE_PATH):
        """
        Initialize the ReportHTMLRenderer.

        Args:
            template_path (str | Path, optional): Path to the directory containing Jinja2 templates.
                Defaults to the internal '_templates' directory.
        """
        self.env = Environment(loader=FileSystemLoader(template_path))
        self.template = self.env.get_template("_default.html")
        self._html_str = None

    def render(self, report_data: dict) -> str:
        """
        Render HTML from a dictionary of report data.

        Args:
            report_data (dict): The report data to render. Should contain a "sections" key with section data.

        Returns:
            str: The rendered HTML as a string.
        """
        self._html_str = self.template.render(sections=report_data.get("sections", {}))
        return self._html_str

    def render_from_json(self, json_path: str | Path) -> str:
        """
        Render HTML from a JSON file containing report data.

        Args:
            json_path (str | Path): Path to the JSON file with report data.

        Returns:
            str: The rendered HTML as a string.
        """
        json_path = Path(json_path)
        with open(json_path, mode="r") as f:
            report_data = json.load(f)
        return self.render(report_data)

    def save_html(self, html_str: str = None, output_path: str | Path = None):
        """
        Save the rendered HTML to a file.

        Args:
            html_str (str, optional): The HTML string to save. If None, uses the last rendered HTML.
            output_path (str | Path, optional): The file path to save the HTML to.

        Raises:
            ValueError: If no HTML has been rendered or output_path is not specified.
        """
        if html_str is None:
            html_str = self._html_str
        if html_str is None:
            raise ValueError("No HTML has been rendered yet. Please call render() or render_from_json() first.")
        if output_path is None:
            raise ValueError("output_path must be specified.")
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, mode="w") as f:
            f.write(html_str)

    @property
    def html_str(self):
        """
        Get the most recently rendered HTML string.

        Returns:
            str or None: The last rendered HTML string, or None if not rendered yet.
        """
        return self._html_str