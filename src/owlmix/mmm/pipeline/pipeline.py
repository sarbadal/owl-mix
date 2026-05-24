from typing import Self

from ..transformers.base import BaseTransformer


class TransformerPipeline:
    def __init__(self, transformers: list[BaseTransformer]):
        self.transformers = transformers

    def fit(self, x: list[float]) -> Self:
        for transformer in self.transformers:
            transformer.fit_transform(x)
        return self

    def transform(self, x: list[float]) -> list[float]:
        for idx, transformer in enumerate(self.transformers):
            # Ensure it's a concrete subclass, not the abstract base
            if type(transformer) is BaseTransformer:
                raise TypeError(f"Step {idx} cannot be the BaseTransformer class.")
                
            x = transformer.transform(x)
        return x