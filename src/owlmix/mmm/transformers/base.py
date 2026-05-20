class BaseTransformer:
    def fit(self, x):
        return self

    def transform(self, x):
        raise NotImplementedError

    def fit_transform(self, x):
        self.fit(x)
        return self.transform(x)
