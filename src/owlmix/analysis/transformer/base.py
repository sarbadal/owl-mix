import pandas as pd

class BaseTransformer:
    def transform(self, series: pd.Series) -> pd.Series:
        raise NotImplementedError("Transform method must be implemented by subclasses.")