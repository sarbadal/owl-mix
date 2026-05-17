import os, sys
import warnings
from pathlib import Path

warnings.simplefilter('ignore', category=UserWarning)

# Add src to the path
CURRENT_DIR = Path(__file__).parent.parent
SRC_DIR = CURRENT_DIR / "src"
sys.path.append(str(SRC_DIR))
#===============================================================================
import pandas as pd
from owlmix.mmm_synth.generator import MMMDataGenerator

def test_mmm_synth():
    config = "../src/owlmix/mmm_synth/presets/config_fmcg.yaml"
    # FMCG
    gen = MMMDataGenerator(config)
    df = gen.generate()

    print(df.head())


if __name__ == "__main__":
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    test_mmm_synth()