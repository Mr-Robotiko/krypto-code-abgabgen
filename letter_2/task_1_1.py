from typing import List


class AuthenticationFunction:
    def __init__(self, n: int = 17):
        self.initial_state: int = 0x524f464c
        self.n: int = n
    def rotate_left(self, x: int) -> int:
        return ((x << self.n) | (x >> (32 - self.n))) & 0xFFFFFFFF

    def rotate_right(self, x: int) -> int:
        return ((x >> self.n) | (x << (32 - self.n))) & 0xFFFFFFFF

    def Q(self, b: int) -> int:
        return b ^ self.rotate_left(b)

    def update(self, s, p):
        b: int = s ^ p
        return self.Q(b = b)
    def H(self, message: str):
        pass


if __name__ == '__main__':
    auth = AuthenticationFunction()
    print(hex(auth.Q(auth.initial_state, 17)))
