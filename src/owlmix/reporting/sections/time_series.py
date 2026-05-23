import os
from typing import Any, Dict
from ...registry.registry import register_section, ANALYZERS_REGISTRY, PLOTTERS_REGISTRY
from .protocol_cls import ReportBuilderProtocol

@register_section("time_series_decomposition")
def build_time_series_decomposition_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
    """
    Builds the Time Series Decomposition section for the report.

    This function retrieves configuration for time series decomposition from the report builder,
    initializes the appropriate plotter class with its parameters, generates the decomposition plots,
    and returns a dictionary containing the paths to the generated images.

    Args:
        report_builder (ReportBuilderProtocol): The report builder instance containing the 
        dataframe and configuration.

    Returns:
        Dict[str, Any]: A dictionary with key 'images' containing paths to the generated decomposition plots.
    """
    config = report_builder.config.time_series_config
    plotter_cls = PLOTTERS_REGISTRY["time_series_decomposition"]["plotter"]
    plotter_params_cls = PLOTTERS_REGISTRY["time_series_decomposition"]["params"]

    plotter_params = plotter_params_cls(
        date_column=config.date_column,
        target_column=config.target_column,
        period=config.period,
        model=config.model,
        dpi=config.dpi,
        figsize=config.figsize,
        filename_prefix=config.filename_prefix
    )

    plotter = plotter_cls(df=report_builder.df, params=plotter_params)
    charts = plotter.plot(
        output_dir=os.path.join(report_builder.config.output_dir, "charts")
    )

    chart_item = {
        "title": "Time Series Decomposition",
        "description": f"Decomposition of time series for target column: {config.target_column}.",
        "alt_text": "Time series decomposition plots",
        "images": {
            "observed": report_builder.image_to_base64(charts["observed"]),
            "trend": report_builder.image_to_base64(charts["trend"]),
            "seasonal": report_builder.image_to_base64(charts["seasonal"]),
            "residuals": report_builder.image_to_base64(charts["residuals"])    
        }
    }
    return {"data": {}, "chart": chart_item}