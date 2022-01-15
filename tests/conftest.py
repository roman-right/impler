import pytest


@pytest.fixture()
def Cls():
    class A:
        outer = 0

        def __init__(self):
            self.internal = 0

        def exists(self):
            return 0

    return A
