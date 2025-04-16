import unittest
from task_1_1 import AuthenticationFunction


class TestAuthenticationFunction(unittest.TestCase):

    def test_inital_case(self):
        auth: AuthenticationFunction = AuthenticationFunction(n = 17)
        self.assertEqual(auth.Q(b = auth.initial_state), 0xded7e2d2)

    def test_hash_from_initial_case(self):
        auth: AuthenticationFunction = AuthenticationFunction(n = 17)
        self.assertEqual(auth.Q(auth.Q(b = auth.initial_state)), 0x1b725f7d)

    def test_hash_from_hash_from_initial_case(self):
        auth: AuthenticationFunction = AuthenticationFunction(n = 17)
        self.assertEqual(auth.Q(auth.Q(auth.Q(auth.initial_state))), 0xa5886999)

    def test_H_empty(self):
        auth: AuthenticationFunction = AuthenticationFunction(n = 17)
        self.assertEqual(auth.H(""), 0xded7e2d2)

    def test_H_A(self):
        auth: AuthenticationFunction = AuthenticationFunction(n = 17)
        self.assertEqual(auth.H("A"), 0x5d725f7f)

    def test_H_AB(self):
        auth: AuthenticationFunction = AuthenticationFunction(n = 17)
        self.assertEqual(auth.H("AB"), 0x5f3b5f7f)

    def test_H_ABC(self):
        auth: AuthenticationFunction = AuthenticationFunction(n = 17)
        self.assertEqual(auth.H("ABC"), 0x5f39137f)

    def test_H_ABCD(self):
        auth: AuthenticationFunction = AuthenticationFunction(n = 17)
        self.assertEqual(auth.H("ABCD"), 0x5f391128)

    def test_H_ABCDE(self):
        auth: AuthenticationFunction = AuthenticationFunction(n = 17)
        self.assertEqual(auth.H("ABCDE"), 0x2f69af58)


if __name__ == '__main__':
    unittest.main()