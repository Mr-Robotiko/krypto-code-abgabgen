from main import Schiffy128
import unittest


class TestExtensionAttack(unittest.TestCase):

    def test_s_0(self):
        schiffy: Schiffy128 = Schiffy128()
        schiffy.s_box()
        self.assertEqual(schiffy.s0, 170)

    def test_s_1(self):
        schiffy: Schiffy128 = Schiffy128()
        schiffy.s_box(1)
        self.assertEqual(schiffy.s0, 155)

    def test_s_2(self):
        schiffy: Schiffy128 = Schiffy128()
        schiffy.s_box(2)
        self.assertEqual(schiffy.s0, 112)

    def test_s_123(self):
        schiffy: Schiffy128 = Schiffy128()
        schiffy.s_box(123)
        self.assertEqual(schiffy.s0, 33)

    def test_s_255(self):
        schiffy: Schiffy128 = Schiffy128()
        schiffy.s_box(255)
        self.assertEqual(schiffy.s0, 205)


if __name__ == '__main__':
    unittest.main()