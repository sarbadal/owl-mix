import os
from ..registry.registry import (
    register_section,
    ANALYZERS_REGISTRY,
    PLOTTERS_REGISTRY
)

@register_section("acf_pacf")
def build_acf_pacf_section(report_builder: 'ReportBuilder') -> Dict[str, Any]:
    config = report_builder.config.acf_pacf_config
    analyzer_cls = ANALYZERS_REGISTRY["acf_pacf"]["analyzer"]
    plotter_cls = PLOTTERS_REGISTRY["acf_pacf"]["analyzer"]
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

    analyzer = analyzer_cls(report_builder.df, analyzer_params)
    data = analyzer.compute()

    plotter = plotter_cls(data=data, params=plotter_params)
    path = plotter.generate(os.path.join(report_builder.config.output_dir, "charts"))
    chart_item = {
        "title": "ACF and PACF Plots",
        "description": f"ACF and PACF plots for columns: {', '.join(config.columns)} with {config.n_lags} lags.",
        "alt_text": "ACF and PACF plots",
        "image": report_builder.image_to_base64(path)
    }

    return {"data": data, "chart": chart_item}