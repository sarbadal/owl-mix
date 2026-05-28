"""
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
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

DEFAULT_TEMPLATE_PATH = Path(__file__).parent / "_templates"
STATIC_PATH = Path(__file__).parent / "_static"

class ReportHTMLRenderer:
    """
    Renders HTML reports from structured data using Jinja2 templates.
    This class provides methods to render HTML from a Python dictionary or a JSON file,
    and to save the rendered HTML to disk. It is designed for use in automated EDA or analytics
    pipelines where reports need to be generated programmatically.
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

    def get_rendered_html(self) -> str:
        """
        Get the most recently rendered HTML string.
        Returns:
            str: The last rendered HTML string.
        Raises:
            ValueError: If no HTML has been rendered yet.
        """
        if not hasattr(self, "html_str_"):
            raise ValueError(
                "No HTML has been rendered yet. "
                "Please call render() or render_from_json() first."
            )
        return self.html_str_

    def _get_css_content(self, css_path: str | Path = STATIC_PATH / "report.css") -> str:
        """
        Read the content of a CSS file.
        Args:
            css_path (str | Path): The path to the CSS file.
        Returns:
            str: The content of the CSS file as a string.
        """
        css_path = Path(css_path)
        if not css_path.is_file():
            return ""
        with open(css_path, mode="r") as f:
            return f.read()

    def render(self, report_data: dict) -> str:
        """
        Render HTML from a dictionary of report data.
        Args:
            report_data (dict): 
                The report data to render. Should contain a 
                "sections" key with section data.
        Returns:
            str: The rendered HTML as a string.
        """
        now = datetime.now()
        html_str = self.template.render(
            css=self._get_css_content(),
            sections=report_data.get("sections", {}), 
            year=now.year,
            report_datetime=now.strftime("%Y-%m-%d %H:%M:%S")
        )
        self.html_str_ = html_str
        return html_str

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
        if html_str is None and not hasattr(self, "html_str_"):
            raise ValueError(
                "No HTML has been rendered yet. "
                "Please call render() or render_from_json() first."
            )
        html_str = self.html_str_ if html_str is None else html_str
        if output_path is None:
            raise ValueError("output_path must be specified.")
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, mode="w", encoding="utf-8") as f:
            f.write(html_str)

    @property
    def html_str(self):
        """
        Get the most recently rendered HTML string.
        Returns:
            str or None: The last rendered HTML string, or None if not rendered yet.
        """
        return self.html_str_ if hasattr(self, "html_str_") else None