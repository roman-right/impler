from typing import Type

import pytest

from impl_pattern import __version__
from impl_pattern.main import impl, impl_classmethod, impl_staticmethod, \
    impl_interface

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def Cls():
    class A:
        outer = 0

        def __init__(self):
            self.internal = 0

    return A


@pytest.fixture
def Interface():
    class Smth:
        value = 500
        _protected_val = 0


        def _protected_method(self):
            return 0

        def __magic_method__(self):


        def get_100(self):
            return 100

        @classmethod
        def get_101(cls):
            return 101

        @staticmethod
        def get_102():
            return 102

        async def get_103(self):
            return 103

        @classmethod
        async def get_104(cls):
            return 104

        @staticmethod
        async def get_105():
            return 105

    return Smth


def test_version():
    assert __version__ == '0.1.0'


def test_sync_method(Cls):
    @impl(Cls)
    def set_ten(self):
        self.internal = 10

    a = Cls()
    a.set_ten()
    assert a.internal == 10


def test_sync_classmethod(Cls):
    @impl_classmethod(Cls)
    def set_ten(cls: Type[Cls]):
        cls.outer = 10

    Cls.set_ten()
    assert Cls.outer == 10


def test_sync_staticmethod(Cls):
    @impl_staticmethod(Cls)
    def get_ten():
        return 10

    assert Cls.get_ten() == 10


async def test_async_method(Cls):
    @impl(Cls)
    async def set_ten(self: Cls):
        self.internal = 10

    a = Cls()
    await a.set_ten()
    assert a.internal == 10


async def test_async_classmethod(Cls):
    @impl_classmethod(Cls)
    async def set_ten(cls: Type[Cls]):
        cls.outer = 10

    await Cls.set_ten()
    assert Cls.outer == 10


async def test_async_staticmethod(Cls):
    @impl_staticmethod(Cls)
    async def get_ten():
        return 10

    assert await Cls.get_ten() == 10


async def test_interface_as_parent(Cls, Interface):
    class Sample(Cls):
        ...

    s = Sample()

    @impl_interface(Sample, as_parent=True)
    class New(Interface):
        ...

    assert isinstance(s, New)
    assert issubclass(Sample, New)
    assert s.get_100() == 100
    assert Sample.get_101() == 101
    assert Sample.get_102() == 102
    assert await s.get_103() == 103
    assert await Sample.get_104() == 104
    assert await Sample.get_105() == 105
    assert Sample.value == 500


async def test_interface_as_parent_inherited_from_object(Cls, Interface):
    with pytest.raises(TypeError):
        @impl_interface(Cls, as_parent=True)
        class New(Interface):
            ...

async def