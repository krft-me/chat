import unittest
import main as run


class TestInterface(unittest.TestCase):

    def test__basic_version(self):
        self.assertTrue(hasattr(run, '__prg_version__'))
        self.assertNotEqual(run.__prg_version__, '0.0.0')

    def test__basic_name(self):
        self.assertTrue(hasattr(run, '__prg_name__'))
        self.assertNotEqual(run.__prg_name__, '')


if __name__ == '__main__':
    unittest.main()
