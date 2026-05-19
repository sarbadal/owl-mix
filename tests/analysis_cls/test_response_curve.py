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
from owlmix.analysis.response_curve import ResponseCurveAnalyzer, ResponseCurveConfig
from owlmix.analysis.response_curve import adstock, hill

def test_response_curve_analyzer():
    df = create_sample_data(n=100)
    params = ResponseCurveConfig(
        model_type="linear",
        feature_columns=["radio_spend", "digital_spend"],
        target_column="target",
        transformations={
            "radio_spend": lambda x: np.log(x + 1),
            "digital_spend": hill
        },
        baseline="mean"
    )
    analyzer = ResponseCurveAnalyzer(df, params)
    response_curve_json = analyzer.generate_response_curve_json("radio_spend")
    print(response_curve_json)

if __name__ == "__main__":    
    test_response_curve_analyzer()