import unittest
from main import iterated_squares


class TestIteratedSquaresAlgorithm(unittest.TestCase):

    def test_5_pow_11_mod_13(self):
        self.assertEqual(iterated_squares(5,11,13), 8)

    def test_17_pow_19_mod_23(self):
        self.assertEqual(iterated_squares(17,19,23), 5)


if __name__ == '__main__':
    unittest.main()