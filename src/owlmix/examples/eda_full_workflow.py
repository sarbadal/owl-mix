# src/owlmix/examples/eda_full_workflow.py

import pandas as pd
import numpy as np
 
from owlmix.eda import EDAAnalyzer
 
 
def generate_data():
    np.random.seed(0)
    n = 120
 
    df = pd.DataFrame({
        "date": pd.date_range(start="2022-01-01", periods=n, freq="W"),
        "sales": np.random.normal(500, 50, n),
        "tv_spend": np.random.uniform(100, 300, n),
        "radio_spend": np.random.uniform(50, 200, n)
    })
 
    return df
 
 
def main():
    df = generate_data()
 
    eda = EDAAnalyzer(df, target="sales")
 
    # Basic stats
    stats = eda.basic_stats()
    print("\n=== BASIC STATS ===")
    print(stats)
 
    # Correlation
    corr = eda.correlation()
    print("\n=== CORRELATION ===")
    print(corr)
 
    # Lag correlation
    lag_corr = eda.lag_correlation(
        column="tv_spend",
        lags=[1, 2, 3, 4]
    )
    print("\n=== LAG CORRELATION (TV Spend vs Sales) ===")
    print(lag_corr)
 
    # Summary export
    report = eda.summary()
    with open("eda_report.txt", "w") as f:
        f.write(report)
 
    print("\nEDA report saved to eda_report.txt")
 
 
if __name__ == "__main__":
    main()
 