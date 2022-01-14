from enum import Enum, unique
from inspect import isclass
from typing import Callable, Awaitable, Union, Type


@unique
class SubjectType(Enum):
    METHOD = 0
    CLASS_METHOD = 1
    STATIC_METHOD = 2
    INTERFACE = 3


class impl:
    def __init__(
            self,
            target: Type,
            *,
            override: bool = False,
            inject_parent: bool = False,
            copy_protected: bool = False,
            copy_magic: bool = False,
            as_classmethod: bool = False,
            as_staticmethod: bool = False
    ):
        self.target = target
        self.override = override
        self.subject = None

        self.inject_parent = inject_parent
        self.copy_protected = copy_protected
        self.copy_magic = copy_magic

        self.as_classmethod = as_classmethod
        self.as_staticmethod = as_staticmethod

    def detect_subject_type(self) -> SubjectType:
        if isclass(self.subject):
            return SubjectType.INTERFACE
        elif isinstance(self.subject, classmethod):
            return SubjectType.CLASS_METHOD
        elif isinstance(self.subject, staticmethod):
            return SubjectType.STATIC_METHOD
        else:
            return SubjectType.METHOD

    def register_method(self):
        if self.subject_type in [SubjectType.STATIC_METHOD,
                                 SubjectType.CLASS_METHOD]:
            name = self.subject.__func__.__name__
        else:
            name = self.subject.__name__
        if self.override or not hasattr(self.target, name):
            setattr(self.target, name, self.subject)

    def _inject_parent(self):
        if self.target.__bases__ == (object,):
            raise TypeError(
                "Parent injection to the object-based classes is impossible")
        else:
            if self.override:
                self.target.__bases__ = (self.subject,) + self.target.__bases__
            else:
                self.target.__bases__ += (self.subject,)

    def _stick_attributes(self):
        for attr_name in dir(self.subject):
            is_protected = attr_name.startswith("_")
            is_private = attr_name.startswith(
                "__") and not attr_name.endswith("__")
            is_magic = attr_name.startswith("__") and attr_name.endswith(
                "__")
            is_present = hasattr(self.target, attr_name)
            if (not is_protected or self.copy_protected) and (
                    not is_magic or self.copy_magic) and (not is_private) and (
                    not is_present or self.override):
                setattr(self.target, attr_name,
                        getattr(self.subject, attr_name))

    def register_interface(self):
        if self.inject_parent:
            self._inject_parent()
        else:
            self._stick_attributes()

    def convert_subject(self):
        if self.as_classmethod:
            self.subject = classmethod(self.subject)
        elif self.as_staticmethod:
            self.subject = staticmethod(self.subject)

    def __call__(self, subject: Union[Callable, Awaitable, Type]):
        self.subject = subject
        self.convert_subject()
        self.subject_type = self.detect_subject_type()
        if self.subject_type in [SubjectType.METHOD, SubjectType.STATIC_METHOD,
                                 SubjectType.CLASS_METHOD]:
            self.register_method()
        else:
            self.register_interface()
        return subject


