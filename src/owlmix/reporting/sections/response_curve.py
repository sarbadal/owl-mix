import os
from typing import Any, Dict
from ...registry.registry import register_section, ANALYZERS_REGISTRY, PLOTTERS_REGISTRY
from .protocol_cls import ReportBuilderProtocol


@register_section("response_curve")
def build_response_curve_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
    """
    Builds the Response Curve section for the report.

    This function retrieves configuration for response curve analysis from the report builder,
    initializes the appropriate analyzer class with its parameters, computes the response curves,
    generates the corresponding plots, and returns a dictionary containing both the computed data and chart metadata (including a base64-encoded image).

    Args:
        report_builder (ReportBuilderProtocol): The report builder instance containing the 
        dataframe and configuration.

    Returns:
        Dict[str, Any]: A dictionary with keys 'data' (the computed response curve results)
                        and 'chart' (metadata and image for the generated plot).
    """
    config = report_builder.config.response_curve_config
    analyzer_cls = ANALYZERS_REGISTRY["response_curve"]["analyzer"]
    analyzer_params_cls = ANALYZERS_REGISTRY["response_curve"]["params"]
    plotter_cls = PLOTTERS_REGISTRY["response_curve"]["plotter"]
    plotter_params_cls = PLOTTERS_REGISTRY["response_curve"]["params"]

    analyzer_params = analyzer_params_cls(
        model=config.model,
        feature_columns=config.feature_columns,
        target_column=config.target_column,
        transformers=config.transformers,
        curve_type=config.curve_type,
        add_default_transformers=config.add_default_transformers
    )

    analyzer = analyzer_cls(df=report_builder.df, params=analyzer_params)
    data = analyzer.fit(num_points=100, generate_curves=True)

    plotter_params = plotter_params_cls(
        line_color=config.line_color,
        fitted_line_color=config.fitted_line_color,
        label_color=config.label_color
    )

    chart_item = {
        "title": "Response Curves",
        "description": f"Response curves for target column: {config.target_column}.",
        "alt_text": "Response curves",
        "images": {}
    }

    for feature in config.feature_columns:
        curve = data[feature]
        plotter = plotter_cls(curve=curve, params=plotter_params)
        response_curve_path = plotter.plot(
            output_dir=os.path.join(report_builder.config.output_dir, "charts")
        )

        chart_item["images"][feature] = report_builder.image_to_base64(response_curve_path)

    return {"data": data, "chart": chart_item}