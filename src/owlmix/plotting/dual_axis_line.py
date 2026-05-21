import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Any, List, Dict, Optional, Self
from tabulate import tabulate

from ..analysis.transformer.difference import DifferenceTransformer
from ..analysis.transformer.lag import LagTransformer
from ..analysis.transformer.adstock import AdstockTransformer

adstock_transformer = AdstockTransformer(decay_rate=0.5)
diff_transformer = DifferenceTransformer(period=1)
lag_transformer = LagTransformer(lag=1)

TRANSFORMER_FACTORIES = {
    "adstock": lambda: AdstockTransformer(decay_rate=0.5),
    "difference": lambda: DifferenceTransformer(period=1),
    "lag": lambda: LagTransformer(lag=1),
}

def apply_transformation(series: pd.Series, transformer_name: str, lag: int = 0) -> pd.Series:
    factory = TRANSFORMER_FACTORIES.get(transformer_name)
    if factory is None:
        return series
    transformer = factory()
    if lag > 0:
        transformer.lag = lag
    return transformer.transform(series.copy(deep=True))


@dataclass
class DualAxisLineDataConfig:
    time_column: str
    target_column: str
    feature_column: str
    smoothing_method: str = "rolling",  # "rolling" | "ema" | None
    window: int = 3
    normalize: bool = True


class DualAxisLinePreparer:
    RESAMPLE_RULES = {
        100: "YE",     # Yearly
        80: "QE",     # Quarterly
        50: "ME",     # Monthly
        0: "W-MON",  # Weekly
    }

    def __init__(self, df: pd.DataFrame, config: DualAxisLineDataConfig):
        self.df = df.copy(deep=True)
        self.config = config

    def _pick_resample_rule(self, n: int, max_points: int) -> str:
        for factor, rule in sorted(self.RESAMPLE_RULES.items(), reverse=True):
            if n > factor * max_points:
                return rule
        return "W-MON"

    def _sort(self) -> Self:
        self.df[self.config.time_column] = pd.to_datetime(self.df[self.config.time_column], errors="coerce")
        self.df = self.df.dropna(subset=[self.config.time_column])
        self.df = self.df.sort_values(by=self.config.time_column)
        return self

    def apply_transformation(self, transformer_name: str, lag: int = 0) -> Self:
        self.df[self.config.feature_column] = apply_transformation(
            self.df[self.config.feature_column].copy(deep=True), 
            transformer_name, 
            lag
        )
        return self

    def _clean(self) -> Self:
        self.df = self.df[[self.config.time_column, self.config.target_column, self.config.feature_column]]
        self.df = self.df.dropna()
        return self

    def _resample(self, max_points: int = 50) -> Self:
        n = len(self.df)
        if n <= max_points:
            return self

        self.df = self.df.set_index(self.config.time_column)
        rule = self._pick_resample_rule(n, max_points)
        self.df = self.df.resample(rule).mean().dropna().reset_index()
        return self

    def _smooth_series(self, series: pd.Series) -> pd.Series:
        if self.config.smoothing_method == "rolling":
            return series.rolling(window=self.config.window, min_periods=1).mean()
        if self.config.smoothing_method == "ema":
            return series.ewm(span=self.config.window, adjust=False).mean()
        return series  

    def _apply_smoothing(self) -> Self:
        self.df["kpi_smooth"] = self._smooth_series(self.df[self.config.target_column])
        self.df["feature_smooth"] = self._smooth_series(self.df[self.config.feature_column])
        return self

    def _normalize_series(self, series: pd.Series) -> pd.Series:
        min_val = series.min()
        max_val = series.max()
        if max_val - min_val == 0:
            return np.zeros(len(series))
        return (series - min_val) / (max_val - min_val)  

    def _apply_normalization(self) -> Self:
        if self.config.normalize:
            self.df["kpi_norm"] = self._normalize_series(self.df["kpi_smooth"])
            self.df["feature_norm"] = self._normalize_series(self.df["feature_smooth"])
            return self
        self.df["kpi_norm"] = self.df["kpi_smooth"]
        self.df["feature_norm"] = self.df["feature_smooth"]
        return self

    def _generate_points(self, series: pd.Series, width: float, height: float, left_pad: float, top_pad: float) -> str:
        n = len(series)
        if n == 0:
            return ""
 
        step = width / (n - 1) if n > 1 else 0
 
        points = []
        for i, val in enumerate(series):
            x = left_pad + i * step
            y = top_pad + height * (1 - val)
            points.append(f"{x},{y}")
 
        return " ".join(points)

    def _build_output(self, width: float, height: float, left_pad: float, top_pad: float) -> Dict[str, Any]:
        chart_width = width
        chart_height = height
 
        return {
            "time": self.df[self.config.time_column].astype(str).tolist(),
 
            "kpi": {
                "raw": self.df[self.config.target_column].tolist(),
                "smooth": self.df["kpi_smooth"].tolist(),
                "normalized": self.df["kpi_norm"].tolist(),
                "min": float(self.df[self.config.target_column].min()),
                "max": float(self.df[self.config.target_column].max()),
                "points": self._generate_points(
                    self.df["kpi_norm"], chart_width, chart_height, left_pad, top_pad
                ),
            },
 
            "feature": {
                "raw": self.df[self.config.feature_column].tolist(),
                "smooth": self.df["feature_smooth"].tolist(),
                "normalized": self.df["feature_norm"].tolist(),
                "min": float(self.df[self.config.feature_column].min()),
                "max": float(self.df[self.config.feature_column].max()),
                "points": self._generate_points(
                    self.df["feature_norm"], chart_width, chart_height, left_pad, top_pad
                ),
            },
        }

    def prepare(self, width: int = 300, height: int = 80, left_pad: int = 30, top_pad: int = 10) -> Dict[str, Any]:
        return (
            self._sort()
                ._clean()
                ._resample()
                ._apply_smoothing()
                ._apply_normalization()
                ._build_output(width, height, left_pad, top_pad)
        )

 