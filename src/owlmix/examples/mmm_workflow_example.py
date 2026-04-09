# src/owlmix/examples/mmm_workflow_example.py

import pandas as pd
import numpy as np
 
from owlmix.transform.pipeline import TransformPipeline
from owlmix.eda import EDAAnalyzer
from owlmix.utils.cleanup import final_cleanup
 
 
def generate_mmm_data():
    np.random.seed(42)
    n = 150
 
    df = pd.DataFrame({
        "date": pd.date_range(start="2022-01-01", periods=n, freq="W"),
        "sales": np.random.normal(1000, 100, n),
        "tv_spend": np.random.uniform(200, 500, n),
        "digital_spend": np.random.uniform(100, 300, n),
        "radio_spend": np.random.uniform(50, 150, n)
    })
 
    return df
 
 
def main():
    df = generate_mmm_data()
 
    print("\n=== ORIGINAL DATA ===")
    print(df.head())
 
    # -------------------------
    # Step 1: Transformations
    # -------------------------
    pipeline = TransformPipeline()
 
    # TV transformations
    pipeline.add_lag("tv_spend", lag=1)
    pipeline.add_adstock("tv_spend", decay=0.6)
    pipeline.add_saturation("tv_spend", method="hill", k=300, s=2)
 
    # Digital transformations
    pipeline.add_adstock("digital_spend", decay=0.4)
    pipeline.add_saturation("digital_spend", method="log")
 
    df_transformed = pipeline.run(df)
 
    # -------------------------
    # Step 2: Cleanup
    # -------------------------
    df_clean = final_cleanup(df_transformed)
 
    print("\n=== TRANSFORMED DATA ===")
    print(df_clean.head())
 
    # -------------------------
    # Step 3: EDA
    # -------------------------
    eda = EDAAnalyzer(df_clean, target="sales")
 
    print("\n=== BASIC STATS ===")
    print(eda.basic_stats())
 
    print("\n=== CORRELATION ===")
    print(eda.correlation())
 
    print("\n=== LAG CORRELATION (TV) ===")
    print(eda.lag_correlation("tv_spend", lags=[1, 2, 3]))
 
    # -------------------------
    # Step 4: Export report
    # -------------------------
    report = eda.summary()
 
    with open("mmm_eda_report.txt", "w") as f:
        f.write(report)
 
    print("\nMMM EDA report saved to mmm_eda_report.txt")
 
 
if __name__ == "__main__":
    main()
 