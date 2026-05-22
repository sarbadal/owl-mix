from typing import Callable, Dict, Any, Optional
from ..analysis.base import BaseAnalyzer
from ..plotting.base import BasePlotter
from ..analysis.acf_pacf import AcfPacfAnalyzer, AcfPacfParams
from ..analysis.box_plot import BoxPlotAnalyzer, BoxParams
from ..analysis.causality import CausalityAnalyzer, CausalityParams
from ..analysis.vif import VIFAnalyzer, VIFParams
from ..analysis.correlation import CorrelationAnalyzer, CorrelationParams
from ..plotting.acf_pacf import AcfPacfPlotter, AcfPacfPlotParams
from ..plotting.box_plot import BoxPlotter, BoxPlotParams
from ..plotting.dual_axis_line import DualAxisLinePreparer, DualAxisLineDataConfig
from ..plotting.vif import VIFPlotter, VIFPlotParams
from ..plotting.correlation import CorrelationPlotter, CorrPlotParams
from ..analysis.ccf import CCFAnalyzer, CCFParams
from ..mmm.analysis.response_curve import ResponseCurveAnalyzer, ResponseCurveParams
from ..mmm.visualization.plotter import ResponsePlotter, ResponsePlotConfig
from ..mmm.visualization.marginal_roi import MarginalROIPlotter, MarginalROIPlotConfig
from ..mmm.analysis.summary import ResponseSummary, SummaryParams

SectionBuilder = Callable[..., Dict[str, Any]]

ANALYZERS_REGISTRY: dict[str, dict[str, type[BaseAnalyzer] | type]] = {
    "acf_pacf": {"analyzer": AcfPacfAnalyzer, "params": AcfPacfParams},
    "vif": {"analyzer": VIFAnalyzer, "params": VIFParams},
    "correlation": {"analyzer": CorrelationAnalyzer, "params": CorrelationParams},
    "box_plot": {"analyzer": BoxPlotAnalyzer, "params": BoxParams},
    "causality": {"analyzer": CausalityAnalyzer, "params": CausalityParams},
    "ccf": {"analyzer": CCFAnalyzer, "params": CCFParams},
    "response_curve": {"analyzer": ResponseCurveAnalyzer, "params": ResponseCurveParams},
    "response_summary": {"analyzer": ResponseSummary, "params": SummaryParams},
}

PLOTTERS_REGISTRY: dict[str, dict[str, type[BasePlotter] | type]] = {
    "acf_pacf": {"plotter": AcfPacfPlotter, "params": AcfPacfPlotParams},
    "vif": {"plotter": VIFPlotter, "params": VIFPlotParams},
    "correlation": {"plotter": CorrelationPlotter, "params": CorrPlotParams},
    "box_plot": {"plotter": BoxPlotter, "params": BoxPlotParams},
    "dual_axis_line": {"plotter": DualAxisLinePreparer, "params": DualAxisLineDataConfig},
    "response_curve": {"plotter": ResponsePlotter, "params": ResponsePlotConfig},
    "marginal_roi": {"plotter": MarginalROIPlotter, "params": MarginalROIPlotConfig},
}

SECTION_BUILDERS: Dict[str, SectionBuilder] = {}

def register_section(name: str):
    def decorator(func: SectionBuilder):
        SECTION_BUILDERS[name] = func
        return func
    return decorator