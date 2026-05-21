import os, sys
import warnings
from pathlib import Path

warnings.simplefilter('ignore', category=UserWarning)

# Add src to the path
CURRENT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = CURRENT_DIR / "src"
sys.path.append(str(SRC_DIR))
#===============================================================================
import pandas as pd
from owlmix.mmm.transformers.adstock import AdstockTransformer

def test_adstock_transformer():
    # Sample data
    df = pd.DataFrame({
        "media_spend": [100, 150, 200, 250, 300]
    })

    # Adstock transformation with a decay rate of 0.5
    adstock = AdstockTransformer(decay=0.5)
    transformed = adstock.transform(df["media_spend"])

    print("Original media spend:", df["media_spend"].tolist())
    print("Adstock transformed spend:", transformed.tolist())


if __name__ == "__main__":
    test_adstock_transformer()