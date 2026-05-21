import numpy as np
from typing import Dict
 
 
class ResponseCurveClassifier:
    """Classifies response curve into zones based on marginal ROI thresholds"""
    def __init__(self, curve: Dict, low_ratio: float = 0.3, high_ratio: float = 0.7):
        self.curve = curve
        self.low_ratio = low_ratio
        self.high_ratio = high_ratio
 
    def classify(self):
        x = np.array(self.curve["input_value"])
        y = np.array(self.curve["predicted_target"])
 
        marginal = np.gradient(y, x)
        max_m = np.max(marginal)
 
        low = self.low_ratio * max_m
        high = self.high_ratio * max_m
 
        zones = []
 
        for m in marginal:
            if m >= high:
                zones.append("underspend")
            elif m >= low:
                zones.append("optimal")
            else:
                zones.append("saturated")
 
        return {
            "zones": zones,
            "marginal": marginal.tolist(),
            "thresholds": {"low": float(low), "high": float(high)}
        }