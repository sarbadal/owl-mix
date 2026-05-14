import os
from ...registry.registry import register_section, ANALYZERS_REGISTRY, PLOTTERS_REGISTRY
from .protocol_cls import ReportBuilderProtocol


@register_section("causality")
def build_causality_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
    """
    Builds the causality analysis section for the report.

    This function retrieves configuration for causality analysis from the report builder,
    initializes the appropriate analyzer and plotter classes with their parameters,
    computes the causality results, generates the corresponding plots, and returns a dictionary
    containing both the computed data and chart metadata (including a base64-encoded image).

    Args:
        report_builder (ReportBuilderProtocol): The report builder instance containing the 
        dataframe and configuration.

    Returns:
        Dict[str, Any]: A dictionary with keys 'data' (the computed causality results)
                        and 'chart' (metadata and image for the generated plot).
    """
    config = report_builder.config.causality_config
    analyzer_cls = ANALYZERS_REGISTRY["causality"]["analyzer"]
    # plotter_cls = PLOTTERS_REGISTRY["causality"]["plotter"]
    analyzer_params_cls = ANALYZERS_REGISTRY["causality"]["params"]
    # plotter_params_cls = PLOTTERS_REGISTRY["causality"]["params"]

    analyzer_params = analyzer_params_cls(
        target_column=config.target_column,
        columns=config.columns,
        max_lag=config.max_lag,
        precision=config.precision,
        error_threshold=config.error_threshold,
        p_value_weight=config.p_value_weight,
        mape_weight=config.mape_weight
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
    #     "title": "Granger Causality Analysis",
    #     "description": f"Granger causality analysis for target column: {config.target_column} with max lag of {config.max_lag}.",
    #     "alt_text": "Granger causality analysis plots",
    #     "image": report_builder.image_to_base64(path)
    # }

    return {"data": data, "chart": None}