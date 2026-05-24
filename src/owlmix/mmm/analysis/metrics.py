import numpy as np

class ResponseMetrics:
    """Utility class for response curve metrics"""

    def __init__(self, curve: dict):
        self.curve = curve
        self.contribution = np.array(curve["contribution"]["contribution"])
        self.x = np.array(curve["input_value"])
        self.y = np.array(curve["predicted_target"])

    def current_spend(self):
        """Latest spend level"""
        # return float(self.x[-1])
        return float(self.curve.get("observed_input_max", self.x[-1]))

    def average_spend(self, window=None):
        """Average spend"""
        min_x = float(self.curve.get("observed_input_min", np.nanmin(self.x)))
        max_x = float(self.curve.get("observed_input_max", np.nanmax(self.x)))

        observed_x = self.x[(self.x >= min_x) & (self.x <= max_x)]
        if observed_x.size == 0:
            observed_x = np.array([min_x, max_x], dtype=float)

        if window:
            observed_x = observed_x[-window:]

        return float(np.mean(observed_x))

    def roi(self):
        """Average ROI"""
        spend = np.sum(self.x)
        if spend == 0:
            return 0.0
        contribution = np.sum(self.contribution)
        return float(contribution / spend)

    def marginal_roi(self):
        """Marginal ROI curve (dy/dx)"""
        return np.gradient(self.y, self.x)

    def current_marginal_roi(self):
        """Marginal ROI at current spend"""
        marginal = self.marginal_roi()
        idx = np.argmin(np.abs(self.x - self.current_spend()))
        return float(marginal[idx])

    def peak_marginal_roi(self):
        """Maximum marginal ROI"""
        marginal = self.marginal_roi()
        return float(np.max(marginal))

    def saturation_point(self, threshold_ratio=0.2):
        """
        Spend level where marginal ROI falls below threshold
        """
        marginal = self.marginal_roi()
        peak = np.max(marginal)
        threshold = peak * threshold_ratio
        below = np.where(marginal < threshold)[0]
        if len(below) == 0:
            return None
        return float(self.x[below[0]])

    def efficiency_ratio(self):
        """Current marginal ROI / peak marginal ROI"""
        current = self.current_marginal_roi()
        peak = self.peak_marginal_roi()
        if peak == 0:
            return 0.0
        return float(current / peak)

    def classify_status(self, high_threshold=0.7, low_threshold=0.3):
        """Underinvested / Optimal / Saturated based on efficiency ratio"""
        ratio = self.efficiency_ratio()

        # Mapping thresholds to status (ordered from high to low !IMPORTANT)
        config = {
            high_threshold: "underinvested",
            low_threshold: "optimal",
        }
        for threshold, status in config.items():
            if ratio >= threshold:
                return status
        return "saturated"

    def summary(self):
        return {
            "current_spend": self.current_spend(),
            "average_spend": self.average_spend(),
            "roi": self.roi(),
            "current_marginal_roi": self.current_marginal_roi(),
            "peak_marginal_roi": self.peak_marginal_roi(),
            "saturation_point": self.saturation_point(),
            "efficiency_ratio": self.efficiency_ratio(),
            "status": self.classify_status(),
        }