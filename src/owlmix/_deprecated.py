import warnings
from functools import wraps
 

def deprecated(replacement: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            warnings.warn(
                f"{func.__name__}() is deprecated and will be removed in a future version. "
                f"Use {replacement}() instead.",
                DeprecationWarning,
                stacklevel=2
            )
            return getattr(self, replacement)(*args, **kwargs)
        return wrapper
    return decorator
