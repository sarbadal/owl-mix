import pandas as pd
import numpy as np
 
 
class ContributionAnalyzer:
    def __init__(self, df: pd.DataFrame, model, feature_cols):
        self.df = df.copy()
        self.model = model
        self.feature_cols = feature_cols
 
    def feature_contribution(self, df, feature):
        """Contribution using prediction difference when feature is zeroed out"""
        # Full prediction
        full_pred = self.model.predict(df[self.feature_cols])
 
        # Remove feature
        modified = df.copy()
        modified[feature] = 0
 
        reduced_pred = self.model.predict(modified[self.feature_cols]) 
        contribution = full_pred - reduced_pred
        return contribution
 
    def total_contribution(self, df, feature):
        contrib = self.feature_contribution(df, feature)
        return float(np.sum(contrib))
 
    def average_contribution(self, df, feature):
        contrib = self.feature_contribution(df, feature)
        return float(np.mean(contrib))

    def summary(self, df, feature):
        return {
            "contribution": self.feature_contribution(df, feature).tolist(),
            "total_contribution": self.total_contribution(df, feature),
            "average_contribution": self.average_contribution(df, feature),
        }
 