from typing import Callable, Dict, Any, Optional
from ..analysis.base import BaseAnalyzer
from ..plotting.base import BasePlotter
from ..analysis.acf_pacf import AcfPacfAnalyzer, AcfPacfParams
from ..analysis.vif import VIFAnalyzer, VIFParams
from ..plotting.acf_pacf import AcfPacfPlotter, AcfPacfPlotParams
from ..plotting.vif import VIFPlotter, VIFPlotParams

SectionBuilder = Callable[..., Dict[str, Any]]

ANALYZERS_REGISTRY: dict[str, dict[str, type[BaseAnalyzer] | type]] = {
    "acf_pacf": {"analyzer": AcfPacfAnalyzer, "params": AcfPacfParams},
    "vif": {"analyzer": VIFAnalyzer, "params": VIFParams},
}

PLOTTERS_REGISTRY: dict[str, dict[str, type[BasePlotter] | type]] = {
    "acf_pacf": {"plotter": AcfPacfPlotter, "params": AcfPacfPlotParams},
    "vif": {"plotter": VIFPlotter, "params": VIFPlotParams},
}

SECTION_BUILDERS: Dict[str, SectionBuilder] = {}

def register_section(name: str):
    def decorator(func: SectionBuilder):
        SECTION_BUILDERS[name] = func
        return func
    return decorator