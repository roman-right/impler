from typing import Type

import pytest

from impl_pattern import __version__
from impl_pattern.main import impl, impl_classmethod, impl_staticmethod

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def Cls():
    class A:
        outer = 0

        def __init__(self):
            self.internal = 0

    return A


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
