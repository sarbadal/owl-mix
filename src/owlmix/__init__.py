import sys
import warnings

from . import transform
from . import eda
from . import report
from . import examples

__all__ = [
    "transform",
    "eda",
    "report",
    "examples"
]

MIN_PYTHON = (3, 14)

warnings.warn(
    "This version of owlmix is in development stage and may be unstable. "
    "Consider using version >= 1.0.0 for a stable release.",
    category=UserWarning,
    stacklevel=2,
)

if sys.version_info < MIN_PYTHON:
    major, minor = MIN_PYTHON
    warnings.warn(
        f"If you are using Python {sys.version_info.major}.{sys.version_info.minor} "
        f"This package is tested on Python {major}.{minor} "
        "Some features may not be supported.",
        category=UserWarning,
        stacklevel=2,
    )