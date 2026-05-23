import os
from typing import Any, Dict
from ...registry.registry import register_section, ANALYZERS_REGISTRY, PLOTTERS_REGISTRY
from .protocol_cls import ReportBuilderProtocol

@register_section("response_summary")
def build_response_summary_section(report_builder: ReportBuilderProtocol) -> Dict[str, Any]:
    """
    Builds the Response Summary section for the report.

    This function retrieves configuration for response summary analysis from the report builder,
    initializes the appropriate analyzer class with its parameters, computes the response summary,
    and returns a dictionary containing the computed summary data.

    Args:
        report_builder (ReportBuilderProtocol): The report builder instance containing the 
        dataframe and configuration.

    Returns:
        Dict[str, Any]: A dictionary with key 'data' containing the computed response summary results.
    """
    config = report_builder.config.response_summary_config
    analyzer_cls = ANALYZERS_REGISTRY["response_summary"]["analyzer"]
    analyzer_params_cls = ANALYZERS_REGISTRY["response_summary"]["params"]
    plotter_cls = PLOTTERS_REGISTRY["response_curve"]["plotter"]
    plotter_params_cls = PLOTTERS_REGISTRY["response_curve"]["params"]
    marginal_roi_plotter_cls = PLOTTERS_REGISTRY["marginal_roi"]["plotter"]
    marginal_roi_plotter_params_cls = PLOTTERS_REGISTRY["marginal_roi"]["params"]

    analyzer_params = analyzer_params_cls(
        model=config.model,
        feature_columns=config.feature_columns,
        target_column=config.target_column,
        transformers=config.transformers,
        curve_type=config.curve_type,
        add_default_transformers=config.add_default_transformers
    )

    analyzer = analyzer_cls(df=report_builder.df, params=analyzer_params)
    data = analyzer.generate()

    plotter_params = plotter_params_cls(
        line_color=config.line_color,
        fitted_line_color=config.fitted_line_color,
        label_color=config.label_color
    )

    chart_item = {
        "title": "Response Curves",
        "description": f"Response curves for target column: {config.target_column}.",
        "alt_text": "Response curves",
        "images": {
            "response_curve": {},
            "marginal_roi": {}  
        }
    }

    for feature in config.feature_columns:
        curve = data[feature]["curve"]
        current_spend=data[feature]["metrics"]["current_spend"]
        plotter = plotter_cls(curve=curve, current_spend=current_spend, params=plotter_params)
        marginal_roi_plotter = marginal_roi_plotter_cls(
            curve=curve, 
            classification=data[feature]["classification"], 
            params=plotter_params
        )
        response_curve_path = plotter.plot(
            output_dir=os.path.join(report_builder.config.output_dir, "charts")
        )
        chart_item["images"]["response_curve"][feature] = report_builder.image_to_base64(response_curve_path)
        marginal_roi_path = marginal_roi_plotter.plot(
            output_dir=os.path.join(report_builder.config.output_dir, "charts")
        )
        chart_item["images"]["marginal_roi"][feature] = report_builder.image_to_base64(marginal_roi_path)

    return {"data": data, "chart": chart_item}
