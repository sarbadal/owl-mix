import os
from ...registry.registry import register_section, ANALYZERS_REGISTRY, PLOTTERS_REGISTRY
from .protocol_cls import ReportBuilderProtocol


@register_section("vif")
def build_vif_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
    """
    Builds the VIF section for the report.

    This function retrieves configuration for VIF analysis from the report builder,
    initializes the appropriate analyzer and plotter classes with their parameters,
    computes the VIF data, generates the corresponding plot, and returns a dictionary
    containing both the computed data and chart metadata (including a base64-encoded image).

    Args:
        report_builder (ReportBuilderProtocol): The report builder instance containing the 
        dataframe and configuration.

    Returns:
        Dict[str, Any]: A dictionary with keys 'data' (the computed VIF results)
                        and 'chart' (metadata and image for the generated plot).
    """
    config = report_builder.config.vif_config
    analyzer_cls = ANALYZERS_REGISTRY["vif"]["analyzer"]
    plotter_cls = PLOTTERS_REGISTRY["vif"]["plotter"]
    analyzer_params_cls = ANALYZERS_REGISTRY["vif"]["params"]
    plotter_params_cls = PLOTTERS_REGISTRY["vif"]["params"]

    analyzer_params = analyzer_params_cls(
        target_column=config.target_column,
        features=config.features,
        precision=config.precision,
        color_thresholds=config.color_thresholds
    )
    plotter_params = plotter_params_cls()

    analyzer = analyzer_cls(
        df=report_builder.df,
        params=analyzer_params
    )
    data = analyzer.compute()

    plotter = plotter_cls(data=data, params=plotter_params)
    path = plotter.generate(os.path.join(report_builder.config.output_dir, "charts"))
    features_str = "all features" if config.features is None else ", ".join(config.features)
    chart_item = {
        "title": "VIF Plot",
        "description": f"VIF plot for target column: {config.target_column} with features: {features_str}.",
        "alt_text": "VIF plot",
        "image": report_builder.image_to_base64(path)
    }

    return {"data": data, "chart": chart_item}