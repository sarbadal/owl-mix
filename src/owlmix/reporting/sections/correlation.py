import os
from ...registry.registry import register_section, ANALYZERS_REGISTRY, PLOTTERS_REGISTRY
from .protocol_cls import ReportBuilderProtocol


@register_section("correlation")
def build_correlation_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
    """
    Builds the Correlation section for the report.

    This function retrieves configuration for correlation analysis from the report builder,
    initializes the appropriate analyzer and plotter classes with their parameters,
    computes the correlation matrix and lagged correlations, generates the corresponding plots,
    and returns a dictionary containing both the computed data and chart metadata (including a base64-encoded image).

    Args:
        report_builder (ReportBuilderProtocol): The report builder instance containing the 
        dataframe and configuration.

    Returns:
        Dict[str, Any]: A dictionary with keys 'data' (the computed correlation results)
                        and 'chart' (metadata and image for the generated plot).
    """
    config = report_builder.config.correlation_config
    analyzer_cls = ANALYZERS_REGISTRY["correlation"]["analyzer"]
    plotter_cls = PLOTTERS_REGISTRY["correlation"]["plotter"]
    analyzer_params_cls = ANALYZERS_REGISTRY["correlation"]["params"]
    plotter_params_cls = PLOTTERS_REGISTRY["correlation"]["params"]

    analyzer_params = analyzer_params_cls(
        columns=config.columns,
        n_lags=config.n_lags,
        precision=config.precision
    )
    plotter_params = plotter_params_cls()

    analyzer = analyzer_cls(
        df=report_builder.df,
        params=analyzer_params
    )
    data = analyzer.compute()

    plotter = plotter_cls(data=data, params=plotter_params)
    corr_path, lagged_corr_path = plotter.generate(os.path.join(report_builder.config.output_dir, "charts"))
    columns_str = ", ".join(config.columns) if config.columns else "all columns"
    chart_item = {
        "title": "Correlation Matrix and Lagged Correlations",
        "description": f"Correlation matrix and lagged correlations for columns: {columns_str} with {config.n_lags} lags.",
        "alt_text": "Correlation matrix and lagged correlations",
        "images": {
            "correlation_matrix": report_builder.image_to_base64(corr_path),
            "lagged_correlation_matrix": report_builder.image_to_base64(lagged_corr_path)
        }
    }

    return {"data": data, "chart": chart_item}