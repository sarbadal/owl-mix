import os
from ...registry.registry import register_section, ANALYZERS_REGISTRY, PLOTTERS_REGISTRY
from .protocol_cls import ReportBuilderProtocol


@register_section("acf_pacf")
def build_acf_pacf_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
    """
    Builds the ACF and PACF section for the report.

    This function retrieves configuration for ACF/PACF analysis from the report builder,
    initializes the appropriate analyzer and plotter classes with their parameters,
    computes the ACF/PACF data, generates the corresponding plots, and returns a dictionary
    containing both the computed data and chart metadata (including a base64-encoded image).

    Args:
        report_builder (ReportBuilderProtocol): The report builder instance containing the 
        dataframe and configuration.

    Returns:
        Dict[str, Any]: A dictionary with keys 'data' (the computed ACF/PACF results)
                        and 'chart' (metadata and image for the generated plot).
    """
    config = report_builder.config.acf_pacf_config
    analyzer_cls = ANALYZERS_REGISTRY["acf_pacf"]["analyzer"]
    plotter_cls = PLOTTERS_REGISTRY["acf_pacf"]["plotter"]
    analyzer_params_cls = ANALYZERS_REGISTRY["acf_pacf"]["params"]
    plotter_params_cls = PLOTTERS_REGISTRY["acf_pacf"]["params"]

    analyzer_params = analyzer_params_cls(
        columns=config.columns,
        n_lags=config.n_lags,
        precision=config.precision
    )
    plotter_params = plotter_params_cls(
        acf_marker=config.acf_marker,
        pacf_marker=config.pacf_marker,
        acf_stem=config.acf_stem,
        pacf_stem=config.pacf_stem,
        acf_conf=config.acf_conf,
        pacf_conf=config.pacf_conf,
    )

    analyzer = analyzer_cls(
        df=report_builder.df,
        params=analyzer_params
    )
    data = analyzer.compute()

    plotter = plotter_cls(data=data, params=plotter_params)
    path = plotter.generate(os.path.join(report_builder.config.output_dir, "charts"))
    columns_str = ", ".join(config.columns) if config.columns else "all columns"
    chart_item = {
        "title": "ACF and PACF Plots",
        "description": f"ACF and PACF plots for columns: {columns_str} with {config.n_lags} lags.",
        "alt_text": "ACF and PACF plots",
        "image": report_builder.image_to_base64(path)
    }

    return {"data": data, "chart": chart_item}