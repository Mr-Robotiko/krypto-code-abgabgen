from main import Schiffy128
import unittest


class TestExtensionAttack(unittest.TestCase):

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

    def test_k_1(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.keys[1], 0x56df778000000000000005d6b532cd00)

    def test_k_2(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.keys[2], 0xdde00000000000000175ad4cb3ebd858)

    def test_k_31(self):
        schiffy: Schiffy128 = Schiffy128()
        self.assertEqual(schiffy.keys[31], 0x770feb4b3180dc3bc09870bd38e2cb5f)

    def test_zero_block(self):
        schiffy: Schiffy128 = Schiffy128()


if __name__ == '__main__':
    unittest.main()