import os, sys
import warnings
from pathlib import Path

warnings.simplefilter('ignore', category=UserWarning)

# Add src to the path
CURRENT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = CURRENT_DIR / "src"
sys.path.append(str(SRC_DIR))
#===============================================================================

import pandas as pd
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
    # print(result)

    analyzer.print_results_json(result)
    analyzer.print_results(result)

if __name__ == "__main__":
    # test_vif_analyzer()
    ...

