from typing import Callable, Dict, Any, Optional
from ..analysis.base import BaseAnalyzer
from ..plotting.base import BasePlotter
from ..analysis.acf_pacf import AcfPacfAnalyzer, AcfPacfParams
from ..analysis.vif import VIFAnalyzer, VIFParams
from ..analysis.causality import CausalityAnalyzer, CausalityParams
from ..analysis.correlation import CorrelationAnalyzer, CorrelationParams
from ..plotting.acf_pacf import AcfPacfPlotter, AcfPacfPlotParams
from ..plotting.vif import VIFPlotter, VIFPlotParams
from ..plotting.correlation import CorrelationPlotter, CorrPlotParams

SectionBuilder = Callable[..., Dict[str, Any]]

ANALYZERS_REGISTRY: dict[str, dict[str, type[BaseAnalyzer] | type]] = {
    "acf_pacf": {"analyzer": AcfPacfAnalyzer, "params": AcfPacfParams},
    "vif": {"analyzer": VIFAnalyzer, "params": VIFParams},
    "correlation": {"analyzer": CorrelationAnalyzer, "params": CorrelationParams},
    "causality": {"analyzer": CausalityAnalyzer, "params": CausalityParams},
}

PLOTTERS_REGISTRY: dict[str, dict[str, type[BasePlotter] | type]] = {
    "acf_pacf": {"plotter": AcfPacfPlotter, "params": AcfPacfPlotParams},
    "vif": {"plotter": VIFPlotter, "params": VIFPlotParams},
    "correlation": {"plotter": CorrelationPlotter, "params": CorrPlotParams},
    # No plotter for causality analysis as of now, but can be added in the future
}

SECTION_BUILDERS: Dict[str, SectionBuilder] = {}

def register_section(name: str):
    def decorator(func: SectionBuilder):
        SECTION_BUILDERS[name] = func
        return func
    return decorator