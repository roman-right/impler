## Implements the `impl` pattern*

/* *inspired by Rust*

Useful when it is needed to extend a class (usually 3d party) with some methods

### Install

```shell
pip install impl_pattern
```

or

```shell
poetry add impl_pattern
```

### Usage

#### Regular methods

```python
from impl_pattern import impl

class Sample:
    def __init__(self):
        self.value = 10

@impl(Sample)
def plus_one(self: Sample):
    self.value += 1

s = Sample()
s.plus_one()

print(s.value) 
# 11
```

it works with async methods as well

```python
from asyncio import sleep

@impl(Sample)
async def plus_one(self: Sample):
    await sleep(1)
    self.value += 1

s = Sample()
await s.plus_one()

print(s.value) 
# 11
```

#### Class methods

To register function as a classmethod you can use `impl_classmethod` decorator

```python
from impl_pattern import impl_classmethod

class Sample:
    value = 10

@impl_classmethod(Sample)
def plus_one(cls):
    cls.value += 1

Sample.plus_one()

print(Sample.value) 
# 11
```

This works with async methods too

```python
from asyncio import sleep

@impl_classmethod(Sample)
async def plus_one(cls):
    await sleep(1)
    self.value += 1

await Sample.plus_one()

print(Sample.value) 
# 11
```

#### Static methods

Static methods use the same syntax but with the `impl_staticmethod` decorator

```python
from impl_pattern import impl_staticmethod

class Sample:
    ...

@impl_staticmethod(Sample)
def get_one():
    return 1

print(Sample.get_one()) 
# 1
```

This works with async methods too

```python
from asyncio import sleep

@impl_staticmethod(Sample)
async def get_one():
    return 1

print(await Sample.get_one()) 
# 1
```