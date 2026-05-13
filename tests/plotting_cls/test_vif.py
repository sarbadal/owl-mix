import os, sys
import warnings
from pathlib import Path

warnings.simplefilter('ignore', category=UserWarning)

# Add src to the path
CURRENT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = CURRENT_DIR / "src"
sys.path.append(str(SRC_DIR))
#===============================================================================
from owlmix.plotting.vif import VIFPlotter, VIFPlotParams
from owlmix.utils.sample_data_generator import create_sample_data
from owlmix.analysis.vif import VIFAnalyzer, VIFParams

def test_vif_analyzer():
    df = create_sample_data(n=100)
    params = VIFParams(
        target_column="sales",
        features=["tv_spend", "radio_spend", "digital_spend", "inflation", "digital_imp", "radio_imp"],
        precision=3,
        color_thresholds=[(5, "green"), (10, "orange"), (float("inf"), "red")]
    )
    analyzer = VIFAnalyzer(df, params)
    result = analyzer.compute()
    return result

def test_vif_plotter():
    data = test_vif_analyzer()
    plotter = VIFPlotter(data)
    output_path = plotter.generate()
    print(f"VIF chart saved to: {output_path}")

if __name__ == "__main__":
    test_vif_plotter()
