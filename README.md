Contains AutOperatio, a mixin which makes self-type-returning
operations on instances of subclasses of general purpose built-in containers,
dict, set, list, and tuple, return subclass instances.


Problem:
-------
Subclassing built-in general-purpose containers is messy because an instance of the subclass will often
return an instance of the superclass instead of an instance of itself if an operation is performed on it.

Example:

    class Foo(list):
        pass
    foo = Foo()
    foo += []        # foo is still an instance of Foo, as it's mutated in place
    foo2 = foo + []  # foo2 is just a list!
    foo3 = foo[:]    # foo3 is just a list!

This holds true for all built-in transformative operators which act on sequences and return a similar type:
    [slice], +, -, *, &, ^, |

As well as non-updating set methods:
    union, difference, intersection, symmetric_difference, union


Solution:
--------
Make subclasses of sets, lists, dicts, and tuples which employ default methods and dunders
return an instance of their own class when these operations are performed.

Do this by including AutOperatio as a mixin when subclassing general purpose built-in containers.


Usage:
-----
Inherit from Autoperatio and the class you wish to subclass in the same subclass, like this:

    class Foo(set, AutOperatio):  # This works
        ...
    class SubFoo(Foo):            # This will work too, as will all inheritors if methods aren't overriden
        ...
    class Bar(AutOperatio, set)   # As will this
        ...

Built-in to use methods from must be last thing in in \_\_mro\_\_ other than object or AutoOperatio...
or you need to specify superclass=<class> in the signature of every subclass definition like this:

    class Foo(list, AutOperatio, SomethingElse, superclass=list):  # Must specify or SomethingElse will be used
        ...
    class SubFoo(Foo, superclass=list):                            # Still required or SomethingElse will be used
        ...
    class Bar:
        ...
    class SubBar(AutOperatio, tuple, Bar, superclass=tuple):       # Required here too and in all subclasses
        ...
        
By default, superclass \_\_new\_\_ and \_\_init\_\_ are used for producing new instances. This prevents overriding them
from breaking anything. If this isn't desired behavior, use kwargs in signature of class definitions like this:

    class Foo(list, AutOperatio, super_new=False, super_init=False):
        ...

Differences from collections.UserList and collections.UserDict when used for list and dict:
------------------------------------------------------------------------------------------
- Not wrappers
- Methods do not have to rely on \_\_new\_\_ and \_\_init\_\_ of subclass
- No data, __cast, or any other extra class attributes
- The only apparent addition to subclass over built-ins is \_\_closure\_\_ in redefined methods




Coverage Report:

    Name                  Stmts   Miss  Cover
    -----------------------------------------
    src\autoperatio.py       35      0   100%
    test_autoperatio.py     115      0   100%
    -----------------------------------------
    TOTAL                   150      0   100%
