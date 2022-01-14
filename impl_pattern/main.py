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
            raise TypeError("impl_type is wrong. See _ImplType enum class")
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


def impl_interface(
        cls: Type,
        as_parent=False,
        override=False,
        copy_protected=False,
        copy_magic=False
):
    """
    Decorator.
    Set the class as a parent for the given one
    Args:
        cls: Type
        as_parent: bool - inject interface a parent class
        inject

    Returns: class

    """

    def decorator(interface: Type):
        if as_parent:
            if cls.__bases__ == (object,):
                raise TypeError(
                    "Parent injection to the object-based classes is impossible")
            else:
                if override:
                    cls.__bases__ = (interface,) + cls.__bases__
                else:
                    cls.__bases__ += (interface,)
        else:
            for attr_name in dir(interface):
                is_protected = attr_name.startswith("_")
                is_private = attr_name.startswith(
                    "__") and not attr_name.endswith("__")
                is_magic = attr_name.startswith("__") and attr_name.endswith(
                    "__")
                if True:  # TODO make condition
                    setattr(cls, attr_name, getattr(interface, attr_name))
        return cls

    return decorator
