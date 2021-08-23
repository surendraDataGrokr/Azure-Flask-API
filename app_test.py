import unittest

def add(a,b):
    return a + b


class AddTest(unittest.TestCase):
    def test1(self):
        c = add(5 , 10)
        self.assertEqual(c, 15)

    def test2(self):
        c = add(5, 10)
        self.assertNotEqual(c, 10)