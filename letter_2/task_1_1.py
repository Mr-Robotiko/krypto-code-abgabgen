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

    def update(self, s: int, p: int) -> int:
        b: int = s ^ p
        return self.Q(b = b)

    def block_divider(self, message_bytes):
        i = 0
        while i + 4 <= len(message_bytes):
            block = int.from_bytes(message_bytes[i:i + 4], byteorder = "big")
            self.initial_state = self.update(self.initial_state, block)
            i += 4

        if i < len(message_bytes):
            remaining = message_bytes[i:]
            pad = remaining + b'\xff' * (4 - len(remaining))
            block = int.from_bytes(pad, byteorder = "big")
            self.initial_state = self.update(self.initial_state, block)

    def H(self, message: str) -> int:
        message_bytes = message.encode("utf-8")
        self.block_divider(message_bytes)
        return self.Q(self.initial_state)


if __name__ == '__main__':
    auth = AuthenticationFunction()
    print(hex(auth.H("ABCDEFGHI")))
