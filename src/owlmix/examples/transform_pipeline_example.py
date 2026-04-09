# src/owlmix/examples/transform_pipeline_example.py

import pandas as pd
import numpy as np
 
from owlmix.transform.pipeline import TransformPipeline
from owlmix.utils.cleanup import final_cleanup
 
 
def generate_data():
    np.random.seed(1)
    n = 100
 
    df = pd.DataFrame({
        "sales": np.random.normal(300, 30, n),
        "tv_spend": np.random.uniform(50, 200, n)
    })
 
    return df
 
 
def main():
    df = generate_data()
 
    pipeline = TransformPipeline()
 
    # Add transformations
    pipeline.add_lag(column="tv_spend", lag=1)
    pipeline.add_adstock(column="tv_spend", decay=0.5)
    pipeline.add_saturation(
        column="tv_spend",
        method="hill",
        k=100,
        s=2
    )
 
    df_transformed = pipeline.run(df)
 
    # Cleanup
    df_final = final_cleanup(df_transformed)
 
    print("\n=== TRANSFORMED DATA ===")
    print(df_final.head())
 
 
if __name__ == "__main__":
    main()
 