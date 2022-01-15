from typing import Type

import pytest

from impl_pattern import impl, impl_classmethod, impl_staticmethod
from impl_pattern.main import impl_method

pytestmark = pytest.mark.asyncio


def test_impl_method(Cls):
    @impl_method(Cls)
    def set_ten(self):
        self.internal = 10

    a = Cls()
    a.set_ten()
    assert a.internal == 10


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

    @impl(Cls)
    @classmethod
    def plus_ten(cls: Type[Cls]):
        cls.outer += 10

    Cls.plus_ten()
    assert Cls.outer == 20


def test_sync_staticmethod(Cls):
    @impl_staticmethod(Cls)
    def get_ten():
        return 10

    assert Cls.get_ten() == 10

    @impl(Cls)
    @staticmethod
    def get_zero():
        return 0

    assert Cls.get_zero() == 0


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

    @impl(Cls)
    @classmethod
    async def plus_ten(cls: Type[Cls]):
        cls.outer += 10

    await Cls.plus_ten()
    assert Cls.outer == 20


async def test_async_staticmethod(Cls):
    @impl_staticmethod(Cls)
    async def get_ten():
        return 10

    assert await Cls.get_ten() == 10

    @impl(Cls)
    @staticmethod
    async def get_zero():
        return 0

    assert await Cls.get_zero() == 0


def test_override(Cls):
    c = Cls()

    @impl(Cls)
    def exists(self):
        return 100

    assert c.exists() == 0

    @impl(Cls, override=True)
    def exists(self):
        return 100

    assert c.exists() == 100
