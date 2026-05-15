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
from owlmix.analysis.acf_pacf import AcfPacfAnalyzer, AcfPacfParams
from owlmix.plotting.acf_pacf import AcfPacfPlotter, AcfPacfPlotParams

def test_acf_pacf_analyzer():
    df = create_sample_data(n=100)
    params = AcfPacfParams(
        columns=["sales", "radio_spend", "digital_spend"],
        n_lags=5,
        precision=4
    )
    analyzer = AcfPacfAnalyzer(df, params)
    result = analyzer.compute()

    analyzer.print_results_json(result)
    analyzer.print_results(result)



if __name__ == "__main__":
    test_acf_pacf_analyzer()
