import os
from typing import Any, Dict
from ...registry.registry import register_section, ANALYZERS_REGISTRY, PLOTTERS_REGISTRY
from .protocol_cls import ReportBuilderProtocol


@register_section("box_plot")
def build_box_plot_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
    """
    Builds the Box Plot section for the report.

    This function retrieves configuration for box plot analysis from the report builder,
    initializes the appropriate analyzer and plotter classes with their parameters,
    computes the necessary data for box plots, generates the corresponding plots,
    and returns a dictionary containing both the computed data and chart metadata (including a base64-encoded image).

    Args:
        report_builder (ReportBuilderProtocol): The report builder instance containing
        the dataframe and configuration.
    Returns:
        Dict[str, Any]: A dictionary with keys 'data' (the computed box plot results)
                        and 'chart' (metadata and image for the generated plot).
    """
    config = report_builder.config.box_plot_config
    analyzer_cls = ANALYZERS_REGISTRY["box_plot"]["analyzer"]
    plotter_cls = PLOTTERS_REGISTRY["box_plot"]["plotter"]
    analyzer_params_cls = ANALYZERS_REGISTRY["box_plot"]["params"]
    plotter_params_cls = PLOTTERS_REGISTRY["box_plot"]["params"]

    analyzer_params = analyzer_params_cls(
        columns=config.columns,
        method=config.method,
        threshold=config.threshold,
        precision=config.precision,
    )
    analyzer_params.set_default_threshold()
    plotter_params = plotter_params_cls(
        n_plot_per_row=config.n_plot_per_row
    )

    analyzer = analyzer_cls(
        df=report_builder.df,
        params=analyzer_params
    )
    data = analyzer.compute()

    plotter = plotter_cls(data=data, params=plotter_params)
    box_plot_path = plotter.generate(os.path.join(report_builder.config.output_dir, "charts"))
    columns_str = ", ".join(config.columns) if config.columns else "all columns"
    chart_item = {
        "title": "Box Plot",
        "description": f"Box plot for columns: {columns_str}.",
        "alt_text": "Box plot",
        "images": {
            "box_plot": report_builder.image_to_base64(box_plot_path)
        }
    }

    return {"data": data, "chart": chart_item}