# src/owlmix/report/generator.py
import os
import json
from owlmix.eda.summary import SummaryBuilder
from owlmix.report.renderer import HTMLRenderer
 
 
class OwlMixReport:
 
    def __init__(self, df: "pd.DataFrame", target: str, date_column: str, output_dir: str = "outputs", template_name: str = "report.html", template_path: str = None):
        self.df = df
        self.target = target
        self.date_column = date_column
        self.output_dir = output_dir
        self.template_name = template_name
        self.template_path = template_path
 
        self.chart_dir = os.path.join(output_dir, "charts")

        self.outlier_chart_config = {
            "columns": None,
            "max_cols_per_chart": 4,
            "single_image": True
        }

        os.makedirs(self.chart_dir, exist_ok=True)

    def set_outlier_chart_layout(self, columns: list[str]=None, max_cols_per_chart: int=4, single_image: bool=True) -> Self:
        if not isinstance(max_cols_per_chart, int) or max_cols_per_chart < 1:
            raise ValueError("max_cols_per_chart must be a positive integer")

        self.outlier_chart_config["max_cols_per_chart"] = max_cols_per_chart
        self.outlier_chart_config["single_image"] = single_image
        self.outlier_chart_config["columns"] = columns

        return self
 
    def generate_json(self):
        builder = SummaryBuilder(
            self.df, 
            target=self.target, 
            date_column=self.date_column, 
            output_dir=self.chart_dir
        )

        builder.set_outlier_chart_layout(**self.outlier_chart_config)
 
        builder = builder.add_all()
        report_dict = builder.build()
 
        json_path = os.path.join(self.output_dir, "report.json")
        builder.save(json_path)
 
        return report_dict, json_path
 
    def generate_html(self) -> str:
        report_dict, _ = self.generate_json()
        html_output_path = os.path.join(self.output_dir, "report.html")

        renderer = HTMLRenderer(
            template_name=self.template_name, 
            template_path=self.template_path
        )
        html_output_path = os.path.join(self.output_dir, "report.html")

        renderer.render(report_dict, html_output_path)

        return html_output_path
 
    def run(self):
        self.generate_json()
        self.generate_html()
