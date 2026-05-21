import json
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from tabulate import tabulate
from typing import Self

from ..models.base import BaseModel
from ..models.sklearn import SimpleLinearModelSK
from .s_curve_filler import SCurveFitter
from ..pipeline.pipeline import TransformerPipeline
from ..transformers.adstock import AdstockTransformer
from ..transformers.hill import HillTransformer
from ..transformers.log import LogTransformer
from ...utils.mixin import ColumnMixin

default_transformers_ = TransformerPipeline(
    [
        AdstockTransformer(0.1),
        HillTransformer(50, 1.8)
        # LogTransformer()
    ]
)


@dataclass
class ResponseCurveParams:
    model: BaseModel = None
    feature_columns: list[str] = None
    target_column: str = None
    transformers: dict[str, TransformerPipeline] | None = None
    curve_type: str = "exponential"
    add_default_transformers: bool = True


class ResponseCurveAnalyzer(ColumnMixin):
    def __init__(self, df: pd.DataFrame, params: ResponseCurveParams):
        self.df = df.copy()
        self._params = params
        self.model = self._params.model
        self.feature_cols = [
            col
            for col in  (params.feature_columns)
            if col != self._params.target_column
        ]
        self.target = self._params.target_column
        self.transformers = self._params.transformers or {}
        
        if self._params.add_default_transformers:
            self._add_default_transformers()
        self._validate_transformers()

        if self.model is None:
            self._add_default_model()
        self.curve_type = self._params.curve_type
        self.fitted_models = {}
        self.curves = {}

    def _validate_transformers(self) -> None:
        for feature, transformer in self.transformers.items():
            if transformer is None:
                continue
            if not hasattr(transformer, "transform") or not callable(transformer.transform):
                raise TypeError(
                    f"Invalid transformer for feature '{feature}': "
                    f"{type(transformer).__name__}. Expected object with callable transform(values)."
                )

    def _add_default_model(self) -> Self:
        if self.model is None:
            X = self.df[self.feature_cols]
            y = self.df[self.target]
            self.model = SimpleLinearModelSK().fit(X, y)
        return self

    def _add_default_transformers(self) -> Self:
        for feature in self.feature_cols :
            if feature not in self.transformers:
                self.transformers[feature] = default_transformers_
        return self

    def _apply_transformer(self, feature, values):
        if feature in self.transformers:
            return self.transformers[feature].transform(values)
        return values

    def fit(self, num_points: int = 100, generate_curves: bool = True, clip_negative_target: bool = True, return_raw_target: bool = True, return_uplift: bool = False):
        """
        Fit S-curve for each feature.
        If generate_curves=True, also generate curve data using generate_curve().
        NaN/inf rows are dropped automatically per feature with warning logs.

        Args:
            num_points: Number of points in response curve grid.
            generate_curves: Whether to generate curve data after fit.
            clip_negative_target: If True, floor predicted target at 0.0.
            return_raw_target: If True, include raw predicted target in output.
            return_uplift: If True, include uplift vs baseline (first grid point).

        Returns:
            - dict[str, dict] of curves when generate_curves=True
            - self when generate_curves=False
        """
        print(f"[ResponseCurveAnalyzer] Starting fit for features: {self.feature_cols} with curve type '{self.curve_type}'")
        self.fitted_models = {}
        self.curves = {}

        for feature in self.feature_cols:
            x_raw = pd.to_numeric(self.df[feature], errors="coerce").to_numpy()
            y_raw = pd.to_numeric(self.df[self.target], errors="coerce").to_numpy()
            x_transformed = self._apply_transformer(feature, x_raw)

            if min(x_transformed) < 0:
                print(
                    f"[ResponseCurveAnalyzer][WARN] Feature '{feature}': "
                    f"transformed values contain negatives (min={min(x_transformed):.4f}); "
                    "S-curve fit may fail or produce unreliable results."
                )

            x_transformed = np.asarray(x_transformed, dtype=float)
            y = np.asarray(y_raw, dtype=float) 

            valid_mask = np.isfinite(x_transformed) & np.isfinite(y)
            dropped = int((~valid_mask).sum())

            if dropped > 0:
                print(
                    f"[ResponseCurveAnalyzer][WARN] Feature '{feature}': "
                    f"dropped {dropped} row(s) containing NaN/inf before S-curve fit."
                )

            x_clean = x_transformed[valid_mask]
            y_clean = y[valid_mask]

            if x_clean.size < 3:
                print(
                    f"[ResponseCurveAnalyzer][WARN] Feature '{feature}': "
                    f"not enough valid rows after cleaning (n={x_clean.size}); skipping fit."
                )
                continue

            try:
                print(f"[ResponseCurveAnalyzer] Fitting S-curve for feature '{feature}'")
                fitter = SCurveFitter(func_type=self.curve_type)
                fitter.fit(x_clean, y_clean)
            except Exception as exc:
                print(
                    f"[ResponseCurveAnalyzer][WARN] Feature '{feature}': "
                    f"S-curve fit failed ({exc}); skipping this feature."
                )
                continue

            self.fitted_models[feature] = {
                "fitter": fitter,
                "transformer": self.transformers.get(feature, None),
            }

            if generate_curves:
                try:
                    self.curves[feature] = self.generate_curve(
                        feature=feature,
                        num_points=num_points,
                        clip_negative_target=clip_negative_target,
                        return_raw_target=return_raw_target,
                        return_uplift=return_uplift,
                    )
                except Exception as exc:
                    print(
                        f"[ResponseCurveAnalyzer][WARN] Feature '{feature}': "
                        f"curve generation failed ({exc}); skipping curve output."
                    )

        return self.curves if generate_curves else self

    def _required_model_columns(self) -> list[str]:
        if hasattr(self.model, "coefficients_") and isinstance(self.model.coefficients_, dict):
            return list(self.model.coefficients_.keys())

        if hasattr(self.model, "coefficients") and isinstance(self.model.coefficients, dict):
            return list(self.model.coefficients.keys())

        return list(self.feature_cols)

    def _prepare_prediction_input(self, temp: pd.DataFrame) -> pd.DataFrame:
        required_cols = self._required_model_columns()

        missing = [c for c in required_cols if c not in temp.columns]
        if missing:
            raise ValueError(f"Missing required columns in df for prediction: {missing}")

        x_pred = temp[required_cols].apply(pd.to_numeric, errors="coerce")
        x_pred = x_pred.replace([np.inf, -np.inf], np.nan)
        x_pred = x_pred.dropna(axis=0, how="any")

        if x_pred.empty:
            raise ValueError(
                "No valid rows available for prediction after removing NaN/inf values."
            )

        return x_pred

    def generate_curve(self, feature, num_points=50, clip_negative_target: bool = True, return_raw_target: bool = True, return_uplift: bool = False):
        if feature not in self.df.columns:
            raise ValueError(f"Feature '{feature}' not found in df columns.")

        feature_series = pd.to_numeric(self.df[feature], errors="coerce")
        x_min = np.nanmin(feature_series.values)
        x_max = np.nanmax(feature_series.values)

        if not np.isfinite(x_min) or not np.isfinite(x_max):
            raise ValueError(f"Feature '{feature}' has no finite values to build a curve.")

        grid = np.linspace(x_min, x_max, num_points)

        base_df = self.df.copy()
        raw_results = []

        for val in grid:
            temp = base_df.copy()
            temp[feature] = val

            transformed = self._apply_transformer(feature, temp[feature].values)
            temp[feature] = transformed

            x_pred = self._prepare_prediction_input(temp)
            pred = float(self.model.predict(x_pred).mean())
            raw_results.append(pred)

        raw_arr = np.asarray(raw_results, dtype=float)
        clipped_arr = np.maximum(raw_arr, 0.0)

        if np.any(raw_arr < 0):
            neg_count = int((raw_arr < 0).sum())
            print(
                f"[ResponseCurveAnalyzer][WARN] Feature '{feature}': "
                f"{neg_count}/{len(raw_arr)} curve point(s) had negative predictions."
            )

        final_arr = clipped_arr if clip_negative_target else raw_arr

        curve = {
            "feature": feature,
            "input_value": grid.tolist(),
            "predicted_target": final_arr.tolist(),
            "contribution": {
                "contribution": self.feature_contribution(feature).tolist(),
                "total_contribution": self.total_contribution(feature),
                "average_contribution": self.average_contribution(feature),
            }
        }

        if return_raw_target or clip_negative_target:
            curve["predicted_target_raw"] = raw_arr.tolist()

        if clip_negative_target:
            curve["predicted_target_clipped"] = clipped_arr.tolist()

        if return_uplift:
            baseline = float(final_arr[0])
            curve["predicted_target_uplift"] = (final_arr - baseline).tolist()

        return curve

    def feature_contribution(self, feature: str) -> np.ndarray:
        if feature not in self.df.columns:
            raise ValueError(f"Feature '{feature}' not found in df columns.")

        temp = self.df.copy()
        temp[feature] = 0

        x_pred = self._prepare_prediction_input(temp)
        reduced_pred = self.model.predict(x_pred)

        full_x_pred = self._prepare_prediction_input(self.df)
        full_pred = self.model.predict(full_x_pred)

        contribution = full_pred - reduced_pred
        return contribution

    def total_contribution(self, feature: str) -> float:
        contrib = self.feature_contribution(feature)
        return float(np.sum(contrib))

    def average_contribution(self, feature: str) -> float:
        contrib = self.feature_contribution(feature)
        return float(np.mean(contrib))

    def print_curve(self, curve):
        table = zip(curve["input_value"], curve["predicted_target"], curve["contribution"]["contribution"])
        print(tabulate(table, headers=[curve["feature"], "Predicted Target", "Contribution"], floatfmt=".4f"))

    def print_curve_json(self, curve, indent=2):
        print(json.dumps(curve, indent=indent))
