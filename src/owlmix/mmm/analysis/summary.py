import json
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from tabulate import tabulate
from typing import Self

from ...utils.mixin import ColumnMixin
from .response_curve import ResponseCurveAnalyzer
from .classifier import ResponseCurveClassifier
from .contribution import ContributionAnalyzer
from .metrics import ResponseMetrics
from ..models.base import ModelProtocol
from ..pipeline.pipeline import TransformerPipeline

@dataclass
class SummaryParams:
    """Configuration for summary report formatting"""
    model: ModelProtocol = None
    feature_columns: list[str] = None
    target_column: str = None
    transformers: dict[str, TransformerPipeline] | None = None
    curve_type: str = "exponential"
    add_default_transformers: bool = True


class ResponseSummary(ColumnMixin):
    """
    Generates comprehensive summary for each feature including:
    - Response curve data
    - Classification zones
    - Key metrics (current spend, ROI, marginal ROI, saturation point)
    """
    def __init__(self, df: pd.DataFrame, params: SummaryParams):
        self.df = df.copy()
        self.params = params
        self.feature_columns = [
            col 
            for col in self._get_numeric_columns(params.feature_columns) 
            if col != params.target_column
        ]
        self.response_analyzer = ResponseCurveAnalyzer(
            df=self.df.copy(), params=params
        )

    def generate(self) -> dict:
        curve = self.response_analyzer.fit(num_points=100, generate_curves=True)
        summary = {}
        for feature in self.feature_columns:
            classifier = ResponseCurveClassifier(curve[feature])
            classification = classifier.classify()
            metrics = ResponseMetrics(curve=curve[feature])
            summary[feature] = {
                "curve": curve[feature],
                "classification": classification,
                "metrics": metrics.summary(),
            }
        return summary