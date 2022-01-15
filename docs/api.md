<a id="impl_pattern.main"></a>

# impl\_pattern.main

<a id="impl_pattern.main.impl"></a>

## impl Objects

```python
class impl()
```

Decorator.

Implementation of a method or of an interface for the classes.

<a id="impl_pattern.main.impl.__init__"></a>

#### \_\_init\_\_

```python
def __init__(target: Type, *, override: bool = False, as_parent: bool = False, copy_protected: bool = False, copy_magic: bool = False, as_classmethod: bool = False, as_staticmethod: bool = False)
```

Init

**Arguments**:

  For all:
- `target` - Type
- `override` - bool - should exist attributes and methods be overridden
  For interfaces:
- `as_parent` - bool - inject interface as a parent
- `copy_protected` - bool - copy protected fields *[Works only with inject_parent is Flase]*
- `copy_magic` - bool - copy magic methods and attributes *[Works only with inject_parent is Flase]*
  For methods:
- `as_classmethod` - bool - set method as a class method
- `as_staticmethod` - bool - set method as a static method

<a id="impl_pattern.main.impl_method"></a>

#### impl\_method

```python
def impl_method(target: Type, *, override: bool = False, as_classmethod: bool = False, as_staticmethod: bool = False)
```

Decorator.
Set function as a method of the given class (regular, classmethod or staticmethod)

**Arguments**:

- `target` - Type
- `override` - bool - should exist method be overridden
- `as_classmethod` - bool - set method as a class method
- `as_staticmethod` - bool - set method as a static method

<a id="impl_pattern.main.impl_classmethod"></a>

#### impl\_classmethod

```python
def impl_classmethod(target: Type, *, override: bool = False)
```

Decorator.
Set function as a classmethod of the given class

**Arguments**:

- `target` - Type
- `override` - bool - should exist method be overridden

<a id="impl_pattern.main.impl_staticmethod"></a>

#### impl\_staticmethod

```python
def impl_staticmethod(target: Type, *, override: bool = False)
```

Decorator.
Set function as a staticmethod of the given class

**Arguments**:

- `target` - Type
- `override` - bool - should exist method be overridden

<a id="impl_pattern.main.impl_interface"></a>

#### impl\_interface

```python
def impl_interface(target: Type, *, override: bool = False, as_parent: bool = False, copy_protected: bool = False, copy_magic: bool = False)
```

**Arguments**:

- `target` - Type
- `override` - bool - should exist attributes and methods be overridden
- `as_parent` - bool - inject interface as a parent
- `copy_protected` - bool - copy protected fields [Works only with inject_parent == Flase]
- `copy_magic` - bool - copy magic methods and attributes [Works only with inject_parent == Flase]

