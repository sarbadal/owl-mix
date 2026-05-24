from __future__ import annotations
from typing import Protocol

class ModelProtocol(Protocol):
    def fit(self, X, y): ...
    def predict(self, X): ...

class BaseModel:
    def fit(self, X, y):
        raise NotImplementedError

    def predict(self, X):
        raise NotImplementedError
