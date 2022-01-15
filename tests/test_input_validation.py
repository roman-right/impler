from typing import Type

import pytest

from impl_pattern import impl
from impl_pattern.exceptions import ImplException


def test_incompatible_type(Cls):
    with pytest.raises(ImplException):

        @impl(Cls, as_parent=True)
        def plus_ten(cls: Type[Cls]):
            cls.outer += 10

    with pytest.raises(ImplException):

        @impl(Cls, copy_protected=True)
        def plus_ten(cls: Type[Cls]):
            cls.outer += 10

    with pytest.raises(ImplException):

        @impl(Cls, copy_magic=True)
        def plus_ten(cls: Type[Cls]):
            cls.outer += 10

    with pytest.raises(ImplException):

        @impl(Cls, as_classmethod=True, as_staticmethod=True)
        def plus_ten(cls: Type[Cls]):
            cls.outer += 10

    with pytest.raises(ImplException):

        @impl(Cls, as_classmethod=True)
        @classmethod
        def plus_ten(cls: Type[Cls]):
            cls.outer += 10

    with pytest.raises(ImplException):

        @impl(Cls, as_staticmethod=True)
        class Interface:
            ...

    with pytest.raises(ImplException):

        @impl(Cls, as_classmethod=True)
        class Interface:
            ...

    with pytest.raises(ImplException):

        @impl(Cls, as_parent=True, copy_magic=True)
        class Interface:
            ...

    with pytest.raises(ImplException):

        @impl(Cls, as_parent=True, copy_protected=True)
        class Interface:
            ...
