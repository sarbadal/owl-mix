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
from owlmix.mmm.models.simple_model import SimpleLinearModel
from owlmix.mmm.models.sklearn import SimpleLinearModelSK
from owlmix.mmm.transformers.adstock import AdstockTransformer
from owlmix.mmm.transformers.hill import HillTransformer
from owlmix.mmm.pipeline.pipeline import TransformerPipeline
from owlmix.mmm.analysis.response_curve import ResponseCurveAnalyzer, ResponseCurveParams
from owlmix.mmm.visualization.plotter import ResponsePlotter
from owlmix.mmm.analysis.metrics import ResponseMetrics

def test_response_curve_analyzer():
    # Sample data
    df = create_sample_data(n=500, include_nan=False)
    # Model
    model_ = SimpleLinearModel({"tv_spend": 0.5}, intercept=10)
    sklearn_model = SimpleLinearModelSK().fit(
        X=df[["tv_spend", "digital_spend", "radio_spend", "tv_grp", "digital_imp"]],
        y=df["sales"]
    )

    feature_columns = ["tv_spend", "digital_spend", "radio_spend", "tv_grp", "digital_imp"]
    
    # Transformers
    transformers = {
        "tv_spend": TransformerPipeline([
            AdstockTransformer(0.6),
            HillTransformer(50, 1.8)
        ]),
        "digital_spend": TransformerPipeline([
            AdstockTransformer(0.4),
            HillTransformer(30, 1.5)
        ]),
        "radio_spend": TransformerPipeline([
            AdstockTransformer(0.3),
            HillTransformer(20, 1.2)
        ]),
        "tv_grp": TransformerPipeline([
            AdstockTransformer(0.5),
            HillTransformer(40, 1.6)
        ]),
        # "digital_imp": TransformerPipeline([
        #     AdstockTransformer(0.4),
        #     HillTransformer(30, 1.5)
        # ])
    }

    params = ResponseCurveParams(
        # model=sklearn_model,
        feature_columns=feature_columns,
        target_column="sales",
        # transformers=transformers,
        # add_default_transformers=False
    )
    
    # Analyzer
    analyzer = ResponseCurveAnalyzer(df=df, params=params)
    curves = analyzer.fit(num_points=100, generate_curves=True)
    analyzer.print_curve_json(curve=curves)

    # Summary and Plot
    for feature in feature_columns:
        metrics = ResponseMetrics(curve=curves[feature])
        summary = metrics.summary()
        print(summary)
        print("========================================================================================================")
        plotter = ResponsePlotter(curve=curves[feature])
        plotter.plot()

if __name__ == "__main__":
    test_response_curve_analyzer()