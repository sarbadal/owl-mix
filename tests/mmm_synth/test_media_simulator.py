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
from owlmix.mmm_synth.core.media_simulator import MediaChannelSimulator
from owlmix.mmm_synth.core.collinearity import MulticollinearityInjector

def test_media_simulator():
    config_path = SRC_DIR / "owlmix/mmm_synth/presets/config_fmcg.yaml"
    config_loader = ConfigLoader(config_path)
    config = config_loader.config

    media_simulator = MediaChannelSimulator(config["media_channels"])
    df = media_simulator.simulate(n=50)  # Replace 100 with the desired number of data points

    print("Simulated Media Channel Data: Number of rows =", len(df))
    print(df.head(n=10))

    return df

def test_collinearity_injector(df: pd.DataFrame):
    config_path = SRC_DIR / "owlmix/mmm_synth/presets/config_fmcg.yaml"
    config_loader = ConfigLoader(config_path)
    collinearity_config = config_loader.config["channel_correlations"]

    injector = MulticollinearityInjector(n=len(df), collinearity_config=collinearity_config)
    df = injector.apply(df)
    print("Data after applying multicollinearity:")
    print(df.head(n=10))
    return df


if __name__ == "__main__":
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    df = test_media_simulator()
    test_collinearity_injector(df)
