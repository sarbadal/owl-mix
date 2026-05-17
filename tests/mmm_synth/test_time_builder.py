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
from owlmix.mmm_synth.config.loader import ConfigLoader
from owlmix.mmm_synth.core.time_builder import TimeSeriesBuilder

def test_time_builder():
    config_path = SRC_DIR / "owlmix/mmm_synth/presets/config_fmcg.yaml"
    config_loader = ConfigLoader(config_path)
    config = config_loader.config

    time_builder = TimeSeriesBuilder(config)
    df = time_builder.build()

    print("Generated Time Series Data: Number of rows =", len(df))
    print(df.head(n=10))


if __name__ == "__main__":
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    test_time_builder()
