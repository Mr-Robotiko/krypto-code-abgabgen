from task_2_2 import ExtensionAttack
import unittest


class TestExtensionAttack(unittest.TestCase):

    def test_abcd_ef(self):
        attack: ExtensionAttack = ExtensionAttack(0x632e4e5c, "abcd")
        self.assertEqual(attack.extension_attack("ef"), 0x0f6b8802)

    def test_abcd_efghijk(self):
        attack: ExtensionAttack = ExtensionAttack(0x632e4e5c, "abcd")
        self.assertEqual(attack.extension_attack("efghijk"), 0x2638a819)


if __name__ == '__main__':
    unittest.main()