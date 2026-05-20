from ..transformers.base import BaseTransformer


class TransformerPipeline:
    def __init__(self, transformers: list[BaseTransformer]):
        self.transformers = transformers

    def fit(self, x):
        for transformer in self.transformers:
            transformer.fit_transform(x)
        return self

    def transform(self, x):
        for idx, transformer in enumerate(self.transformers):
            if type(transformer) is BaseTransformer or transformer.__class__.transform is BaseTransformer.transform:
                raise TypeError(
                    f"Pipeline step {idx} is {type(transformer).__name__} with no transform() implementation. "
                    "Use a concrete transformer like AdstockTransformer/HillTransformer/LogTransformer."
                )
            x = transformer.transform(x)
        return x