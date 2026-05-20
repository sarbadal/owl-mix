import numpy as np
 
 
class ResponseCurveClassifier:
    def __init__(self, low_ratio=0.3, high_ratio=0.7):
        self.low_ratio = low_ratio
        self.high_ratio = high_ratio
 
    def classify(self, curve):
        x = np.array(curve["input_value"])
        y = np.array(curve["predicted_target"])
 
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