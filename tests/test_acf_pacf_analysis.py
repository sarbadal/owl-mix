import os, sys
import warnings
from pathlib import Path

warnings.simplefilter('ignore', category=UserWarning)

# Add src to the path
CURRENT_DIR = Path(__file__).parent.parent
SRC_DIR = CURRENT_DIR / "src"
sys.path.append(str(SRC_DIR))

import numpy as np
import pandas as pd
from owlmix.analysis.acf_pacf import AcfPacfAnalyzer, AcfPacfParams

# Sample data
num_rows = 100 
df = pd.DataFrame({
    "sales": np.random.randint(90, 200, size=num_rows).tolist(),
    "spend": np.random.randint(8, 25, size=num_rows).tolist(),
    "impressions": np.random.randint(900, 1500, size=num_rows).tolist(),
    "tv_grp": np.round(np.random.uniform(4, 10, size=num_rows), 1).tolist()
})

# Initialize calculator
acf_pacf_params = AcfPacfParams(columns=["sales", "spend", "impressions", "tv_grp"], n_lags=3, precision=2)
analyzer = AcfPacfAnalyzer(df=df, params=acf_pacf_params)

# Generate ACF & PACF values
result = analyzer.compute()

print("Print the result in formatted JSON")
analyzer.print_results_json(results=result)

print("Print the ACF/PACF analysis result in a tabular format")
analyzer.print_results(results=result)
