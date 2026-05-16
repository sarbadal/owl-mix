import os
from typing import Any, Dict
from ...registry.registry import register_section, ANALYZERS_REGISTRY, PLOTTERS_REGISTRY
from .protocol_cls import ReportBuilderProtocol


@register_section("ccf")
def build_ccf_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
    """
    Builds the Cross-Correlation Function (CCF) analysis section for the report.

    This function retrieves configuration for CCF analysis from the report builder,
    initializes the appropriate analyzer and plotter classes with their parameters,
    computes the CCF results, generates the corresponding plots, and returns a dictionary
    containing both the computed data and chart metadata (including a base64-encoded image).

    Args:
        report_builder (ReportBuilderProtocol): The report builder instance containing the 
        dataframe and configuration.

    Returns:
        Dict[str, Any]: A dictionary with keys 'data' (the computed CCF results)
                        and 'chart' (metadata and image for the generated plot).
    """
    config = report_builder.config.ccf_config
    analyzer_cls = ANALYZERS_REGISTRY["ccf"]["analyzer"]
    # plotter_cls = PLOTTERS_REGISTRY["ccf"]["plotter"]
    analyzer_params_cls = ANALYZERS_REGISTRY["ccf"]["params"]
    # plotter_params_cls = PLOTTERS_REGISTRY["ccf"]["params"]

    analyzer_params = analyzer_params_cls(
        time_column=config.time_column,
        target_column=config.target_column,
        feature_columns=config.feature_columns,
        max_lag=config.max_lag
    )
    # plotter_params = plotter_params_cls()

    analyzer = analyzer_cls(
        df=report_builder.df,
        params=analyzer_params
    )
    data = analyzer.compute()

    # plotter = plotter_cls(data=data, params=plotter_params)
    # path = plotter.generate(os.path.join(report_builder.config.output_dir, "charts"))
    # chart_item = {
    #     "title": "Cross-Correlation Function (CCF) Analysis",
    #     "description": f"CCF analysis for target column: {config.target_column} with max lag of {config.max_lag}.",
    #     "alt_text": "Cross-Correlation Function analysis plots",
    #     "image": report_builder.image_to_base64(path)
    # }

    return {"data": data, "chart": None}