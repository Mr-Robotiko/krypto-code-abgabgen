import unittest
from main import square_and_multiply


class TestIteratedSquaresAlgorithm(unittest.TestCase):

    def test_5_pow_11_mod_13(self):
        self.assertEqual(square_and_multiply(5,11,13), 8)

    def test_17_pow_19_mod_23(self):
        self.assertEqual(square_and_multiply(17,19,23), 5)

    def test_888_pow_333_mod_11111(self):
        self.assertEqual(square_and_multiply(8888, 333, 11111), 6223)


if __name__ == '__main__':
    unittest.main()