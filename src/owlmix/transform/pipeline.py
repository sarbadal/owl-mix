import pandas as pd
from typing import Dict, List, Any
 
from .lags import create_lags
from .addstock import adstock
from .saturation import saturation
from .cleanup import cleanup_data
 
 
class MMMTransformPipeline:
    """
    Pipeline for MMM feature transformations:
    - Lags
    - Adstock
    - Saturation
    """
 
    def __init__(self, config: Dict[str, Any]):
        """
        config example:
        {
            "lags": {
                "columns": ["tv_spend"],
                "lags": [1, 2]
            },
            "adstock": {
                "columns": ["tv_spend"],
                "decay": 0.5
            },
            "saturation": {
                "columns": ["tv_spend"],
                "method": "hill",
                "alpha": 2,
                "gamma": 100
            },
            "cleanup": {
                "drop_na": True,
                "reset_index": True
            }
        }
        """
        self.config = config
 
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
 
        # Step 1: Lags
        if "lags" in self.config:
            cfg = self.config["lags"]
            df = create_lags(
                df,
                columns=cfg["columns"],
                lags=cfg["lags"]
            )
 
        # Step 2: Adstock
        if "adstock" in self.config:
            cfg = self.config["adstock"]
 
            for col in cfg["columns"]:
                new_col = f"{col}_adstock"
                df[new_col] = adstock(df[col], decay=cfg.get("decay", 0.5))
 
        # Step 3: Saturation
        if "saturation" in self.config:
            cfg = self.config["saturation"]
 
            for col in cfg["columns"]:
                new_col = f"{col}_sat"
                df[new_col] = saturation(
                    df[col],
                    method=cfg.get("method", "hill"),
                    alpha=cfg.get("alpha", 1.0),
                    gamma=cfg.get("gamma", 1.0),
                    lam=cfg.get("lam", 0.01),
                )

        # Step 4: Final cleanup
        if "cleanup" in self.config:
            cfg = self.config["cleanup"]

            df = cleanup_data(
                df,
                drop_na=cfg.get("drop_na", True),
                reset_index=cfg.get("reset_index", True)
            )
 
        return df