import os
from typing import Any, Dict
from ...registry.registry import register_section, ANALYZERS_REGISTRY, PLOTTERS_REGISTRY
from .protocol_cls import ReportBuilderProtocol

@register_section("dist_numeric")
def build_dist_numeric_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
    """
    Builds the Distribution of Numerical Columns section for the report.

    This function retrieves configuration for numerical distribution plotting from the report builder,
    initializes the appropriate plotter class with its parameters, generates distribution plots for
    specified numeric columns, and returns a dictionary containing paths to the generated images.

    Args:
        report_builder (ReportBuilderProtocol): The report builder instance containing the 
        dataframe and configuration.

    Returns:
        Dict[str, Any]: A dictionary with key 'images' containing paths to the generated distribution plots.
    """
    config = report_builder.config.dist_numeric_config
    plotter_cls = PLOTTERS_REGISTRY["numerical_distribution"]["plotter"]
    plotter_params_cls = PLOTTERS_REGISTRY["numerical_distribution"]["params"]

    plotter_params = plotter_params_cls(
        columns=config.columns,
        show_normal_curve=config.show_normal_curve,
        dpi=config.dpi,
        figsize=config.figsize,
        filename_prefix=config.filename_prefix
    )

    plotter = plotter_cls(df=report_builder.df, params=plotter_params)
    images = plotter.plot(
        output_dir=os.path.join(report_builder.config.output_dir, "charts")
    )
    chart_item = {
        "title": "Distribution of Numerical Columns",
        "description": "Histograms with optional normal distribution curves for specified numeric columns.",
        "alt_text": "Distribution charts for numeric columns",
        "images": {
            col: report_builder.image_to_base64(path) 
            for col, path in images.items() if path is not None
        }
    }
    return {"data": {}, "chart": chart_item}