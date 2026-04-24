# src/owlmix/eda/eda.py

import pandas as pd

from .summary import SummaryBuilder

class OwlMixEDA_:
    """
    Main entry point for OwlMix EDA.
 
    Example:
        eda = OwlMixEDA(df, target="sales")
        report = eda.report()
    """
 
    def __init__(self, df: pd.DataFrame, target: str = None, output_dir: str = "outputs"):
        self.df = df
        self.target = target
        self.output_dir = output_dir
 
    def report(self, include_charts: bool = True, save: bool = False, filepath: str = None):
        """
        Generate EDA report.
 
        Parameters:
        ----------
        include_charts : bool
            Whether to include charts
        save : bool
            Whether to save report to file
        filepath : str
            Path to save report
 
        Returns:
        -------
        str : formatted EDA report
        """
 
        builder = SummaryBuilder(
            self.df,
            target=self.target,
            output_dir=self.output_dir,
        )
 
        builder = builder.add_all()
 
        # Generate final text
        report_text = builder.build()
 
        # Save if needed
        if save:
            if not filepath:
                filepath = f"{self.output_dir}/eda_report.json"
            builder.save(filepath)

    def to_html(self, include_charts: bool = True, save: bool = False, filepath: str = None):
        """
        Generate EDA report in HTML format.
    
        Parameters:
        ----------
        include_charts : bool
            Whether to include charts
        save : bool
            Whether to save HTML file
        filepath : str
            Path to save HTML
    
        Returns:
        -------
        str : HTML content
        """

        builder = SummaryBuilder(
            self.df,
            target=self.target,
            output_dir=self.output_dir,
        )
    
        # builder = (
        #     builder
        #     .add_basic_info()
        #     .add_missing_summary()
        #     .add_descriptive_stats()
        # )

        builder = builder.add_all()
        if save:
            if not filepath:
                filepath = f"{self.output_dir}/eda_report.json"
            builder.save(filepath)
    
        # chart_paths = builder.chart_paths if include_charts else []
    
        # Convert to HTML
        # html_content = self._convert_to_html(
        #     builder.sections,
        #     chart_paths
        # )
    
        # Save if required
        # if save:
        #     if not filepath:
        #         filepath = f"{self.output_dir}/eda_report.html"
    
        #     import os
        #     os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
        #     with open(filepath, "w") as f:
        #         f.write(html_content)
    
        # return html_content

    def _convert_to_html(self, sections, chart_paths):
        """Convert text sections + charts into HTML format."""
    
        html_parts = [
            "<html>",
            "<head>",
            "<title>OwlMix EDA Report</title>",
            "<style>",
            "body { font-family: Arial; padding: 20px; }",
            "h2 { color: #2c3e50; }",
            "pre { background: #f4f4f4; padding: 10px; }",
            "img { max-width: 800px; margin: 10px 0; }",
            "</style>",
            "</head>",
            "<body>",
            "<h1>🦉 OwlMix EDA Report</h1>",
        ]
    
        # Add text sections
        for section in sections:
            title = section.split("\n")[0]
            content = "\n".join(section.split("\n")[1:])
    
            html_parts.append(f"<h2>{title}</h2>")
            html_parts.append(f"<pre>{content}</pre>")
    
        # Add charts
        if chart_paths:
            html_parts.append("<h2>Charts</h2>")
            for path in chart_paths:
                html_parts.append(f'<img src="{path}" />')
    
        html_parts.append("</body></html>")
    
        return "\n".join(html_parts)
 