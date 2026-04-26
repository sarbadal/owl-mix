import sys
import warnings

from ._version import __version__, VERSION_THRESHOLD

MIN_TESTED_PYTHON = (3, 14)


def check_python_version():
    major, minor = MIN_TESTED_PYTHON

    if __version__ < VERSION_THRESHOLD:
        warnings.warn(
            f"\nThis version of owlmix ({__version__}) is in development stage and may be unstable. "
            f"Consider using version >= {VERSION_THRESHOLD} for a stable release.",
            category=UserWarning,
            stacklevel=2,
        )

    warnings.warn(
        f"\nYou are using Python {sys.version_info.major}.{sys.version_info.minor} "
        f"This package is tested on Python {major}.{minor} "
        "Some features may not work as expected.",
        category=UserWarning,
        stacklevel=2,
    )