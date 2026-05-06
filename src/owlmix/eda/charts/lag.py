# src/owlmix/eda/charts/lag.py
import os
import math
import logging
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import TypedDict, NotRequired, Unpack
from scipy.stats import pearsonr, spearmanr
from sklearn.feature_selection import mutual_info_regression
from statsmodels.stats.diagnostic import acorr_ljungbox

logger = logging.getLogger(__name__)

class LagCorrelationChartArgs(TypedDict):
    output_dir: NotRequired[str]
    column: NotRequired[str]
    lag: NotRequired[int]

class LagCorrelationChart:
    def __init__(self, df: pd.DataFrame, **kwargs: Unpack[LagCorrelationChartArgs]):
        self.df = df
        self.output_dir = kwargs.get("output_dir", "charts")
        self.column = kwargs.get("column")
        self.max_lag = kwargs.get("lag", 2)
        os.makedirs(self.output_dir, exist_ok=True)

    def _analyze_lags(self, series: pd.Series, max_lag: int):
        results = []
        arr = series.values
        for k in range(1, max_lag + 1):
            x = arr[k:]
            y = arr[:-k]
            if len(x) < 2 or len(y) < 2:
                # Not enough data
                results.append({
                    "lag": k,
                    "pearson_corr": np.nan,
                    "spearman_corr": np.nan,
                    "mutual_info": np.nan,
                    "ljungbox_pvalue": np.nan,
                    "interpretation": "Not enough data"
                })
                continue

            # Linear correlation
            pearson_corr, _ = pearsonr(x, y)
            # Monotonic relationship
            spearman_corr, _ = spearmanr(x, y)
            # Mutual information
            try:
                mi = mutual_info_regression(y.reshape(-1, 1), x)[0]
            except Exception:
                mi = np.nan
            # Ljung-Box test
            try:
                lb_pvalue = acorr_ljungbox(arr, lags=[k], return_df=True)['lb_pvalue'].values[0]
            except Exception:
                lb_pvalue = np.nan

            interpretation = []
            if abs(pearson_corr) > 0.5:
                interpretation.append("Strong linear relationship")
            elif abs(pearson_corr) > 0.2:
                interpretation.append("Weak/moderate linear relationship")
            else:
                interpretation.append("No strong linear relationship")

            if pearson_corr > 0.2:
                interpretation.append("Positive correlation")
            elif pearson_corr < -0.2:
                interpretation.append("Negative correlation")

            if abs(pearson_corr) < 0.2 and abs(spearman_corr) > 0.3:
                interpretation.append("Possible nonlinear relationship")

            if mi > 0.1:
                interpretation.append("Dependency exists")
            else:
                interpretation.append("Likely independent")

            if lb_pvalue > 0.05:
                interpretation.append("Consistent with white noise")
            else:
                interpretation.append("Not white noise")

            results.append({
                "lag": k,
                "pearson_corr": pearson_corr,
                "spearman_corr": spearman_corr,
                "mutual_info": mi,
                "ljungbox_pvalue": lb_pvalue,
                "interpretation": "\n".join(interpretation)
            })
        return pd.DataFrame(results)

    def _generate(self):
        if self.max_lag == 1:
            logger.warning(
                "Lag Correlation Chart (scatter plot): minimum lag should be 2. "
                "Chart has been generated for lag 2."
            )

        n = max(self.max_lag, 2)
        n_cols = 2
        n_rows = math.ceil(n / n_cols)

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 6 * n_rows))
        axes = axes.flatten() if n > 1 else [axes]

        series = self.df[self.column]
        stats_df = self._analyze_lags(series, self.max_lag)

        for lag in range(1, n + 1):
            lagged = series.shift(lag)
            df_lag = pd.DataFrame({
                "x": series,
                "y": lagged
            }).dropna()

            ax = axes[lag - 1]
            if df_lag.empty:
                ax.set_title(f"Lag {lag}: No data after lag")
                ax.axis('off')
                continue

            ax.scatter(df_lag["x"], df_lag["y"], alpha=0.6)
            ax.set_xlabel(f"{self.column}")
            ax.set_ylabel(f"{self.column} (lag={lag})")
            row = stats_df[stats_df["lag"] == lag].iloc[0]
            title = (
                f"Lag {lag}\n"
                f"Pearson: {row['pearson_corr']:.2f}, "
                f"Spearman: {row['spearman_corr']:.2f}\n"
                f"MI: {row['mutual_info']:.2f}, Ljung-Box p: {row['ljungbox_pvalue']:.3f}"
            )
            ax.set_title(title)
            ax.annotate(
                row["interpretation"],
                xy=(0.02, 0.02),  # bottom left
                xycoords='axes fraction',
                ha='left',
                va='bottom',
                fontsize=14,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.7)
            )

        for i in range(n, len(axes)):
            axes[i].axis('off')

        plt.tight_layout()
        file_path = os.path.join(self.output_dir, f"lag_correlation_lag1_to_{self.max_lag}.png")
        plt.savefig(file_path, dpi=150)
        plt.close()
        return file_path

    def generate(self):
        """
        Generates lag correlation plots and statistics for lags 1 to max_lag.
        Returns the saved file path.
        """
        return self._generate()
