from typing import Callable, Dict, Any, Optional
from ..analysis.base import BaseAnalyzer
from ..plotting.base import BasePlotter
from ..analysis.acf_pacf import AcfPacfAnalyzer, AcfPacfParams
from ..plotting.acf_pacf import AcfPacfPlotter, AcfPacfPlotParams

SectionBuilder = Callable[..., Dict[str, Any]]

ANALYZERS_REGISTRY: dict[str, dict[str, type[BaseAnalyzer] | type]] = {
    "acf_pacf": {"analyzer": AcfPacfAnalyzer, "params": AcfPacfParams},
}

PLOTTERS_REGISTRY: dict[str, dict[str, type[BasePlotter] | type]] = {
    "acf_pacf": {"analyzer": AcfPacfPlotter, "params": AcfPacfPlotParams},
}

SECTION_BUILDERS: Dict[str, SectionBuilder] = {}

def register_section(name: str):
    def decorator(func: SectionBuilder):
        SECTION_BUILDERS[name] = func
        return func
    return decorator