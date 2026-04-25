import sys
import warnings

from . import transform
from . import eda
from . import report
from . import file_resolver

__all__ = [
    "transform",
    "eda",
    "report",
    "file_resolver",
]

__version__ = "0.2.0"

MIN_PYTHON = (3, 14)
VERSION_THRESHOLD = "1.0.0"

if __version__ < VERSION_THRESHOLD:
    warnings.warn(
        f"\nThis version of owlmix ({__version__}) is in development stage and may be unstable. "
        f"Consider using version >= {VERSION_THRESHOLD} for a stable release.",
        category=UserWarning,
        stacklevel=2,
    )

if sys.version_info < MIN_PYTHON:
    major, minor = MIN_PYTHON
    warnings.warn(
        f"\nIf you are using Python {sys.version_info.major}.{sys.version_info.minor} "
        f"This package is tested on Python {major}.{minor} "
        "Some features may not be supported.\n",
        category=UserWarning,
        stacklevel=2,
    )