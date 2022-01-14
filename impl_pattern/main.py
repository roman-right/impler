import inspect
from enum import Enum
from functools import wraps
from typing import Type, Callable


class _ImplType(str, Enum):
    METHOD = "METHOD"
    CLASS_METHOD = "CLASS_METHOD"
    STATIC_METHOD = "STATIC_METHOD"


def _impl(cls: Type, impl_type: _ImplType):
    def decorator(f: Callable):
        if impl_type == _ImplType.METHOD:
            method = f
        elif impl_type == _ImplType.CLASS_METHOD:
            method = classmethod(f)
        elif impl_type == _ImplType.STATIC_METHOD:
            method = staticmethod(f)
        else:
            raise TypeError("impl_type is wrong. See ImplType enum class")
        setattr(cls, f.__name__, method)

        @wraps(f)
        def sync_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        @wraps(f)
        async def async_wrapper(*args, **kwargs):
            return await f(*args, **kwargs)

        if inspect.iscoroutinefunction(f):
            return async_wrapper
        return sync_wrapper

    return decorator


def impl(cls: Type):
    """
    Decorator.
    Set function as a method for the class objects
    Args:
        cls: Type

    Returns: func

    """
    return _impl(cls, _ImplType.METHOD)


def impl_classmethod(cls: Type):
    """
    Decorator.
    Set function as a classmethod of the given class
    Args:
        cls: Type

    Returns: func

    """
    return _impl(cls, _ImplType.CLASS_METHOD)


def impl_staticmethod(cls: Type):
    """
    Decorator.
    Set function as a staticmethod of the given class
    Args:
        cls: Type

    Returns: func

    """
    return _impl(cls, _ImplType.STATIC_METHOD)
