from unittest import TestCase, main
from src.autoperatio import AutOperatio, _methods


class TestAutOperatio(TestCase):

    def test_slicing(self):
        """Test slicing lists and tuples."""
        for supercls in {list, tuple}:
            class SubClass(AutOperatio, supercls):
                ...

            self.assertIsInstance(SubClass()[:], SubClass)
            self.assertEqual(SubClass([0])[0], 0)

    def test_methods(self):
        """Execute full battery of rigorous subtests."""
        
        for supercls in {list, dict, set, tuple}:

            # Values which can become sets, dicts, or lists
            val1 = [(1, 2)]
            val2 = [(1, 2), (3, 4)]

            if supercls is tuple:
                val1 = (1, 2)
                val2 = (3, 4)

            class SubClass(AutOperatio, supercls):
                ...

            for method in _methods.intersection(dir(supercls)):

                with self.subTest(method=method, supercls=supercls):
                    sub_meth = getattr(SubClass, method)
                    sup_meth = getattr(supercls, method)
                    try:
                        self.assertIsInstance(
                                sub_meth(SubClass(val1), supercls(val2)),
                                SubClass
                        )
                        self.assertEqual(
                            sub_meth(SubClass(val1), SubClass(val2)),
                            sup_meth(supercls(val1), supercls(val2))
                        )
                        a = SubClass(val1)
                        self.assertIsNotNone(a)
                        b = sub_meth(a, a)
                        self.assertIsNot(a, b)
                    except TypeError:
                        self.assertIsInstance(
                            sub_meth(SubClass(val1), 2),
                            SubClass
                        )
                        self.assertEqual(
                            sub_meth(val1, 2),
                            sup_meth(val1, 2)
                        )
                        a = SubClass(val1)
                        self.assertIsNotNone(a)
                        b = sub_meth(a, 2)
                        self.assertIsNot(a, b)

                class SubSubClass(SubClass):
                    """For testing subsubclass behavior and different __new__ and __init__."""
                    counter = 0

                    def __new__(cls):
                        """No args."""
                        cls.counter += 1
                        if supercls is tuple:
                            return super().__new__(cls, val1)
                        return super().__new__(cls)
                    
                    def __init__(self):
                        """No args, sets own value."""
                        self.counter += 1
                        if supercls is tuple:
                            return
                        super().__init__(val1)
                        
                with self.subTest(method=method, supercls=supercls, extra='SubSubClass weird init weird new'):

                    sub_meth = getattr(SubSubClass, method)
                    sup_meth = getattr(supercls, method)
                    try:
                        self.assertIsInstance(
                            sub_meth(SubSubClass(), supercls(val1)),
                            SubSubClass
                        )
                        self.assertEqual(
                            sub_meth(SubSubClass(), SubSubClass()),
                            sup_meth(supercls(val1), supercls(val1))
                        )
                        a = SubSubClass()
                        self.assertIsNotNone(a)
                        b = sub_meth(a, a)
                        self.assertIsNot(a, b)
                        self.assertTrue(SubSubClass.counter in {4, 8})
                    except TypeError:
                        self.assertIsInstance(
                            sub_meth(SubSubClass(), 2),
                            SubSubClass
                        )
                        self.assertEqual(
                            sub_meth(val1, 2),
                            sup_meth(val1, 2)
                        )
                        a = SubSubClass()
                        self.assertIsNotNone(a)
                        b = sub_meth(a, 2)
                        self.assertIsNot(a, b)
                        self.assertTrue(SubSubClass.counter in {3, 6})

                class Foo:
                    """Breaks expected inheritance structure"""

                class SubClass(supercls, AutOperatio, Foo, superclass=supercls):
                    """For testing superclass keyword argument which fixes inheritance"""

                with self.subTest(method=method, supercls=supercls, extra='superclass keyword'):

                    sub_meth = getattr(SubClass, method)
                    sup_meth = getattr(supercls, method)
                    try:
                        self.assertIsInstance(
                                sub_meth(SubClass(val1), supercls(val2)),
                                SubClass
                        )
                        self.assertEqual(
                            sub_meth(SubClass(val1), SubClass(val2)),
                            sup_meth(supercls(val1), supercls(val2))
                        )
                        a = SubClass(val1)
                        self.assertIsNotNone(a)
                        b = sub_meth(a, a)
                        self.assertIsNot(a, b)
                    except TypeError:
                        self.assertIsInstance(
                            sub_meth(SubClass(val1), 2),
                            SubClass
                        )
                        self.assertEqual(
                            sub_meth(val1, 2),
                            sup_meth(val1, 2)
                        )
                        a = SubClass(val1)
                        self.assertIsNotNone(a)
                        b = sub_meth(a, 2)
                        self.assertIsNot(a, b)

                class SubClass(supercls, AutOperatio, super_new=False, super_init=False):
                    """Tests super_new and super_init keywords by incrementing counter."""
                    counter = 0

                    def __new__(cls, *args):
                        cls.counter += 1
                        return super().__new__(cls, *args)

                    def __init__(self, *args):
                        self.counter += 1
                        if supercls is tuple:
                            return
                        super().__init__(*args)

                with self.subTest(method=method, supercls=supercls, extra='False super keywords'):

                    sub_meth = getattr(SubClass, method)
                    sup_meth = getattr(supercls, method)
                    try:
                        self.assertIsInstance(
                                sub_meth(SubClass(val1), supercls(val2)),
                                SubClass
                        )
                        self.assertEqual(
                            sub_meth(SubClass(val1), SubClass(val2)),
                            sup_meth(supercls(val1), supercls(val2))
                        )
                        a = SubClass(val1)
                        self.assertIsNotNone(a)
                        b = sub_meth(a, a)
                        self.assertIsNot(a, b)
                        self.assertEqual(SubClass.counter, 7)
                    except TypeError:
                        self.assertIsInstance(
                            sub_meth(SubClass(val1), 2),
                            SubClass
                        )
                        self.assertEqual(
                            sub_meth(val1, 2),
                            sup_meth(val1, 2)
                        )
                        a = SubClass(val1)
                        self.assertIsNotNone(a)
                        b = sub_meth(a, 2)
                        self.assertIsNot(a, b)
                        self.assertEqual(SubClass.counter, 6)
