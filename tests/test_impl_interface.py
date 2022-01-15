import pytest

from impler import impl, impl_interface
from impler.exceptions import ImplException

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def Cls():
    class A:
        outer = 0

        def __init__(self):
            self.internal = 0

        def exists(self):
            return 0

    return A


@pytest.fixture
def Interface():
    class Smth:
        value = 500
        _protected_val = 0

        def _protected_method(self):
            return 0

        def __magic_method__(self):
            return 0

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

        def exists(self):
            return 100

    return Smth


async def test_interface_as_parent(Cls, Interface):
    class Sample(Cls):
        ...

    s = Sample()

    @impl(Sample, as_parent=True)
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
    assert s.exists() == 0

    assert s._protected_val == 0
    assert s._protected_method() == 0
    assert s.__magic_method__() == 0


async def test_interface_separated_function(Cls, Interface):
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
    assert s.exists() == 0

    assert s._protected_val == 0
    assert s._protected_method() == 0
    assert s.__magic_method__() == 0


async def test_interface_as_parent_override(Cls, Interface):
    class Sample(Cls):
        ...

    s = Sample()

    @impl(Sample, as_parent=True, override=True)
    class New(Interface):
        ...

    assert s.exists() == 100


def test_interface_as_parent_inherited_from_object(Cls, Interface):
    with pytest.raises(ImplException):

        @impl(Cls, as_parent=True)
        class New(Interface):
            ...


async def test_interface_not_as_parent(Cls, Interface):
    class Sample(Cls):
        ...

    s = Sample()

    @impl(Sample, as_parent=False)
    class New(Interface):
        ...

    assert not isinstance(s, New)
    assert not issubclass(Sample, New)
    assert s.get_100() == 100
    assert Sample.get_101() == 101
    assert Sample.get_102() == 102
    assert await s.get_103() == 103
    assert await Sample.get_104() == 104
    assert await Sample.get_105() == 105
    assert Sample.value == 500
    assert s.exists() == 0

    assert not hasattr(s, "_protected_val")
    assert not hasattr(s, "_protected_method")
    assert not hasattr(s, "__magic_method__")


async def test_interface_not_as_parent_override(Cls, Interface):
    class Sample(Cls):
        ...

    s = Sample()

    @impl(Sample, as_parent=False, override=True)
    class New(Interface):
        ...

    assert s.exists() == 100


async def test_interface_not_as_parent_copy_protected(Cls, Interface):
    class Sample(Cls):
        ...

    s = Sample()

    @impl(Sample, as_parent=False, copy_protected=True)
    class New(Interface):
        ...

    assert s._protected_val == 0
    assert s._protected_method() == 0


async def test_interface_not_as_parent_copy_magic(Cls, Interface):
    class Sample(Cls):
        ...

    s = Sample()

    @impl(Sample, as_parent=False, copy_magic=True)
    class New(Interface):
        ...

    assert s.__magic_method__() == 0
