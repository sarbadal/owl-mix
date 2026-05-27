from ..sections.causality import CausalitySection
from ..sections.acf_pacf import AcfPacfSection
from ..sections.box_plot import BoxPlotSection
from ..sections.correlation import CorrelationSection
from ..sections.time_series_decomposition import TimeSeriesDecompositionSection
from ..sections.ccf import CCFSection
from ..sections.dist_numeric import DistributionNumericSection
from ..sections.response_summary import ResponseSummarySection
from ..sections.vif import VIFSection


SECTION_SCHEMA_REGISTRY = {
    "causality": CausalitySection,
    "acf_pacf": AcfPacfSection,
    "box_plot": BoxPlotSection,
    "correlation": CorrelationSection,
    "time_series_decomposition": TimeSeriesDecompositionSection,
    "ccf": CCFSection,
    "dist_numeric": DistributionNumericSection,
    "response_summary": ResponseSummarySection,
    "vif": VIFSection
}