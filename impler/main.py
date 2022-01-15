from enum import Enum, unique
from inspect import isclass
from typing import Callable, Awaitable, Union, Type

from impler.exceptions import ImplException


@unique
class _SubjectType(Enum):
    METHOD = 0
    CLASS_METHOD = 1
    STATIC_METHOD = 2
    INTERFACE = 3


class impl:
    """
    Decorator.

    Implementation of a method or of an interface for the classes.
    """

    def __init__(
        self,
        target: Type,
        *,
        override: bool = False,
        as_parent: bool = False,
        copy_protected: bool = False,
        copy_magic: bool = False,
        as_classmethod: bool = False,
        as_staticmethod: bool = False,
    ):
        """
        Init
        Args:
            For all:
                target: Type
                override: bool - should exist attributes and methods be overridden
            For interfaces:
                as_parent: bool - inject interface as a parent
                copy_protected: bool - copy protected fields *[Works only with inject_parent is Flase]*
                copy_magic: bool - copy magic methods and attributes *[Works only with inject_parent is Flase]*
            For methods:
                as_classmethod: bool - set method as a class method
                as_staticmethod: bool - set method as a static method
        """
        self.target = target
        self.override = override

        self.as_parent = as_parent
        self.copy_protected = copy_protected
        self.copy_magic = copy_magic

        self.as_classmethod = as_classmethod
        self.as_staticmethod = as_staticmethod

        self.subject: Union[Callable, Awaitable, Type, None] = None
        self.subject_type = None

    def _validate_input(self):
        if self.subject_type != _SubjectType.INTERFACE:
            if self.as_parent or self.copy_protected or self.copy_magic:
                raise ImplException(
                    "Incompatible input parameters for the method implementation"
                )
            if self.as_classmethod and self.as_staticmethod:
                raise ImplException(
                    "Implementation can not be and classmethod and static method the same time"
                )
            if self.subject_type != _SubjectType.METHOD and (
                self.as_classmethod or self.as_staticmethod
            ):
                raise ImplException(
                    "Classmethod or staticmethod modifiers can not be applied to the method, which already is classmethod or staticmethod"
                )
        else:
            if self.as_classmethod or self.as_staticmethod:
                raise ImplException(
                    "Incompatible input parameters for the interface implementation"
                )
            if self.as_parent and (self.copy_protected or self.copy_magic):
                raise ImplException(
                    "Input parameters copy_protectd and copy_magic can not be used if interface was injected as a parent"
                )

    def _detect_subject_type(self):
        if isclass(self.subject):
            self.subject_type = _SubjectType.INTERFACE
        elif isinstance(self.subject, classmethod):
            self.subject_type = _SubjectType.CLASS_METHOD
        elif isinstance(self.subject, staticmethod):
            self.subject_type = _SubjectType.STATIC_METHOD
        else:
            self.subject_type = _SubjectType.METHOD

    def _register_method(self):
        if self.subject_type in [
            _SubjectType.STATIC_METHOD,
            _SubjectType.CLASS_METHOD,
        ]:
            name = self.subject.__func__.__name__
        else:
            name = self.subject.__name__
        if self.override or not hasattr(self.target, name):
            setattr(self.target, name, self.subject)

    def _inject_parent(self):
        if self.target.__bases__ == (object,):
            raise ImplException(
                "Parent injection to the object-based classes is impossible"
            )
        else:
            if self.override:
                self.target.__bases__ = (self.subject,) + self.target.__bases__
            else:
                self.target.__bases__ += (self.subject,)

    def _stick_attributes(self):
        for attr_name in dir(self.subject):
            is_magic = attr_name.startswith("__") and attr_name.endswith("__")
            is_private = (
                False
                if is_magic
                else attr_name.startswith("__")
                and not attr_name.endswith("__")
            )
            is_protected = (
                False if is_magic or is_private else attr_name.startswith("_")
            )
            is_present = hasattr(self.target, attr_name)

            if (
                (not is_protected or self.copy_protected)
                and (not is_magic or self.copy_magic)
                and (not is_private)
                and (not is_present or self.override)
            ):
                setattr(
                    self.target, attr_name, getattr(self.subject, attr_name)
                )

    def _register_interface(self):
        if self.as_parent:
            self._inject_parent()
        else:
            self._stick_attributes()

    def _prepare_subject(self):
        if self.as_classmethod:
            self.subject = classmethod(self.subject)
            self.subject_type = _SubjectType.CLASS_METHOD
        elif self.as_staticmethod:
            self.subject = staticmethod(self.subject)
            self.subject_type = _SubjectType.STATIC_METHOD

    def __call__(self, subject: Union[Callable, Awaitable, Type]):
        self.subject = subject
        self._detect_subject_type()

        self._validate_input()
        self._prepare_subject()

        if self.subject_type == _SubjectType.INTERFACE:
            self._register_interface()
        else:
            self._register_method()

        return subject


def impl_method(
    target: Type,
    *,
    override: bool = False,
    as_classmethod: bool = False,
    as_staticmethod: bool = False,
):
    """
    Decorator.
    Set function as a method of the given class (regular, classmethod or staticmethod)
    Args:
        target: Type
        override: bool - should exist method be overridden
        as_classmethod: bool - set method as a class method
        as_staticmethod: bool - set method as a static method
    """
    return impl(
        target=target,
        override=override,
        as_classmethod=as_classmethod,
        as_staticmethod=as_staticmethod,
    )


def impl_classmethod(
    target: Type,
    *,
    override: bool = False,
):
    """
    Decorator.
    Set function as a classmethod of the given class
    Args:
        target: Type
        override: bool - should exist method be overridden
    """
    return impl(target=target, override=override, as_classmethod=True)


def impl_staticmethod(
    target: Type,
    *,
    override: bool = False,
):
    """
    Decorator.
    Set function as a staticmethod of the given class
    Args:
        target: Type
        override: bool - should exist method be overridden
    """
    return impl(target=target, override=override, as_staticmethod=True)


def impl_interface(
    target: Type,
    *,
    override: bool = False,
    as_parent: bool = False,
    copy_protected: bool = False,
    copy_magic: bool = False,
):
    """

    Args:
        target: Type
        override: bool - should exist attributes and methods be overridden
        as_parent: bool - inject interface as a parent
        copy_protected: bool - copy protected fields [Works only with inject_parent == Flase]
        copy_magic: bool - copy magic methods and attributes [Works only with inject_parent == Flase]
    """
    return impl(
        target=target,
        override=override,
        as_parent=as_parent,
        copy_protected=copy_protected,
        copy_magic=copy_magic,
    )
