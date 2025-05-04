from main import Schiffy128
import unittest


class TestSchiffy(unittest.TestCase):

    def test_s_0(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.lookup_table[0], 170)

    def test_s_1(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.lookup_table[1], 155)

    def test_s_2(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.lookup_table[2], 112)

    def test_s_123(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.lookup_table[123], 33)

    def test_s_255(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.lookup_table[255], 205)

    def test_k_0(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.keys[0], 0xdeadbeef000000000000000bad6b3201)

    def test_zero_block(self):
        schiffy: Schiffy128 = Schiffy128()

    def test_F1(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.F(0x0000000000000000, schiffy.keys[0]), 0x94dfb49607c198ab)

    def test_F2(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.F(0x94dfb49607c198ab, schiffy.keys[1]), 0xb0aa7cca50e95fb1)

    def test_F3(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.F(0xb0aa7cca50e95fb1, schiffy.keys[2]), 0x1e9d6324e9783573)

    def test_F4(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.F(0x8a42d7b2eeb9add8, schiffy.keys[3]), 0x01a6283b0f33c8f0)

    def test_F5(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.F(0xc8ef99ba72f8a579, schiffy.keys[29]), 0xf7ffea032144154a)

    def test_F6(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.F(0x81f3d4d01743d570, schiffy.keys[30]), 0x7fac6b4146d4f4c6)

    def test_F7(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.F(0xb743f2fb342c51bf, schiffy.keys[31]), 0x2a66d3471f7cb499)


if __name__ == '__main__':
    unittest.main()