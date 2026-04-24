# owlmix/eda/acf_pacf.py
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf

from .utils import ColumnMixin


class ACFPACFCalculator(ColumnMixin):
    def __init__(self, df: pd.DataFrame, columns: list[str], n_lags: int = 15, precision: int = 3) -> None:
        self.df = df.copy()
        self.columns = self._get_columns(columns)
        self.n_lags = n_lags
        self.precision = precision

    def generate(self) -> dict[str, list[dict]]:
        """Calculate ACF and PACF for each column."""
        results = []

        for col in self.columns:
            series = self.df[col].dropna()
            n_obs = len(series)

            # Compute ACF & PACF
            acf_vals = acf(series, nlags=self.n_lags)
            pacf_vals = pacf(series, nlags=self.n_lags)

            lags = list(range(len(acf_vals)))

            results.append({
                "column": col,
                "n_obs": n_obs,
                "lags": lags,
                "acf": [round(v, self.precision)  for v in acf_vals.tolist()],
                "pacf": [round(v, self.precision)  for v in pacf_vals.tolist()]
            })

        return {
            "data": results
        }