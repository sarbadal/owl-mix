# src/owlmix/examples/eda_basic.py

import pandas as pd
import numpy as np
 
from owlmix.eda import EDAAnalyzer
 
 
def generate_sample_data():
    np.random.seed(42)
    n = 100
 
    df = pd.DataFrame({
        "date": pd.date_range(start="2023-01-01", periods=n, freq="D"),
        "sales": np.random.normal(200, 20, n),
        "tv_spend": np.random.uniform(50, 150, n),
        "digital_spend": np.random.uniform(20, 100, n)
    })
 
    # introduce some missing values
    df.loc[5:10, "tv_spend"] = np.nan
 
    return df
 
 
def main():
    df = generate_sample_data()
 
    eda = EDAAnalyzer(df, target="sales")
 
    print("\n=== BASIC STATS ===")
    print(eda.basic_stats())
 
    print("\n=== CORRELATION MATRIX ===")
    print(eda.correlation())
 
    print("\n=== SUMMARY REPORT ===")
    report = eda.summary()
    print(report)
 
 
if __name__ == "__main__":
    main()