## Implementation pattern*

/* *inspired by Rust*

Useful when it is needed to extend a class (usually 3d party) with some methods
or interfaces

### Install

```shell
pip install impler
```

or

```shell
poetry add impler
```

### Usage

#### Methods implementation

Using implementation pattern you can extend any class (even 3rd party) with
regular, class or static methods.

```python
from impler import impl
from pydantic import BaseModel


@impl(BaseModel)
def fields_count(self: BaseModel):
    return len(self.__fields__)


class Point(BaseModel):
    x: int = 0
    y: int = 1


point = Point()
print(point.fields_count())
```

Class methods

```python
@impl_classmethod(BaseModel)
def fields_count(cls):
    return len(cls.__fields__)


# or

@impl(BaseModel)
@classmethod
def fields_count(cls):
    return len(cls.__fields__)
```

Static methods

```python
@impl_staticmethod(BaseModel)
def zero(cls):
    return 0


# or

@impl(BaseModel)
@staticmethod
def zero(cls):
    return 0
```

Async methods

```python
@impl(BaseModel)
async def zero(cls):
    await asyncio.sleep(1)
    return 0
```

#### Interfaces implementation

The same way you can extend any class with the whole interface

Here is example of the base interface, which

```python
from pathlib import Path


class BaseFileInterfase:
    def dump(self, path: Path):
        ...

    @classmethod
    def parse(cls, path: Path):
        ...
```

This is how you can implement this interface for Pydantic `BaseModel` class:

```python
from impler import impl
from pydantic import BaseModel
from pathlib import Path


@impl(BaseModel, as_parent=True)
class ModelFileInterface(BaseFileInterface):
    def dump(self, path: Path):
        path.write_text(self.json())
        
    @classmethod
    def parse(cls, path: Path):
        return cls.parse_file(path)

```

If `as_parent` parameter is `True` the implementation will be injected to the list of the target class parents.

Then you can check if the class or object implements the interface:

```python
print(issubclass(BaseModel, BaseFileInterfase))
# True

print(issubclass(Point, BaseFileInterfase))
# True

print(isinstance(point, BaseFileInterface))
# True
```

The whole api documentation could be found by the [link](https://github.com/roman-right/impler/docs/api.md)