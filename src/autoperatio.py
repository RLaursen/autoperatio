"""Contains AutOperatio, a mixin which makes self-type-returning
operations on instances of subclasses of general purpose built-in containers,
dict, set, list, and tuple, return subclass instances.

Usage
-----
Inherit from Autoperatio and the class you wish to subclass in the same subclass, like this:

    class Foo(set, AutOperatio):  # This works
        ...
    class SubFoo(Foo):            # This will work too, as will all inheritors if methods aren't overriden
        ...
    class Bar(AutOperatio, set)   # As will this
        ...

Built-in to use methods from must be last thing in in __mro__ other than object or AutoOperatio...
or you need to specify superclass=<class> in the signature of every subclass definition like this:

    class Foo(list, AutOperatio, SomethingElse, superclass=list):  # Must specify or SomethingElse will be used
        ...
    class SubFoo(Foo, superclass=list):                            # Still required or SomethingElse will be used
        ...
    class Bar:
        ...
    class SubBar(AutOperatio, tuple, Bar, superclass=tuple):       # Required here too and in all subclasses
        ...
        
By default, superclass __new__ and __init__ are used for producing new instances. This prevents overriding them
from breaking anything. If this isn't desired behavior, use kwargs in signature of class definitions like this:

    class Foo(list, AutOperatio, super_new=False, super_init=False):
        ...
"""
_methods = {
            '__and__', '__add__', '__mul__', '__or__',
            '__rand__', '__rmul__', '__ror__', '__rsub__',
            '__rxor__', '__sub__', '__xor__', 'difference',
            'intersection', 'symmetric_difference', 'union'
}


class AutOperatio:
    """Mixin, makes operations on subclasses of general purpose built-in containers return subclass instances."""

    def __init_subclass__(cls, superclass=None, super_new=True, super_init=True, **kwargs):
        """Replace methods which would return a copy of the superclass with wrapped version which returns subclass."""
        if superclass is None:
            superclass = [c for c in cls.__mro__ if c not in {object, AutOperatio, cls}][-1]

        for method in _methods.intersection(dir(superclass)):
            setattr(cls, method, _method_closure(method, cls, superclass, super_new, super_init))

        try:
            superclass()[:]
            setattr(cls, '__getitem__', _getitem_closure(cls, superclass, super_new, super_init))
        except TypeError:
            pass


def _method_closure(method, cls, supercls, super_new, super_init):
    """Closure for operation methods which use superclass method but return subclass."""
    _new_ = supercls.__new__ if super_new else cls.__new__
    _init_ = supercls.__init__ if super_init else cls.__init__
    super_method = getattr(supercls, method)

    if getattr(_init_, '__objclass__', ...) is object:
        def _init_(*args):
            """If _init_ comes from object, replace it, as it takes no args and does nothing anyway."""

    def method_wrapper(self, *args, **kwargs):
        """Wrapped to return subclasses instead of superclass."""
        value = super_method(self, *args, **kwargs)
        new = _new_(cls, value)
        _init_(new, value)
        return new

    method_wrapper.__qualname__ = f'AutOperatio wrapped {supercls.__name__}.{method}'
    method_wrapper.__name__ = f'AutOperatio wrapped {supercls.__name__}.{method}'
    return method_wrapper


def _getitem_closure(cls, supercls, super_new, super_init):
    """Closure for __getitem__ slicing."""
    _getitem_ = _method_closure('__getitem__', cls, supercls, super_new, super_init)

    def method_wrapper(self, n):
        """Wrapped to return subclass when sliced instead of superclass."""
        if isinstance(n, slice):
            return _getitem_(self, n)
        else:
            return supercls.__getitem__(self, n)

    method_wrapper.__qualname__ = f'AutOperatio wrapped {supercls.__name__}.__getitem__'
    method_wrapper.__name__ = f'AutOperatio wrapped {supercls.__name__}.__getitem__'

    return method_wrapper
