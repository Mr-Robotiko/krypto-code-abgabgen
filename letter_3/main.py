from typing import Dict, List


class Schiffy128:

    def __init__(self):
        self.s0: int = 170
        self.inital_key: int = 0xdeadbeef000000000000000badc0ffee
        self.keys: List[int] = list()
        self.lookup_table: List[int] = list()

        # Fill lookuptable and the round keys
        self.s_box()
        self.ksa()

    def s_box(self) -> None:
        for x in range(256):
            self.lookup_table.append(170 if x == 0 else (37 * self.lookup_table[x-1] + 9) % 256)

    def rotate_left(self, i: int) -> int:
        if i == 0:
            return self.inital_key
        else:
            return ((self.keys[i-1] << (7 * i) % 128) | (self.keys[i-1] >> (128 - (7 * i) % 128))) & ((1 << 128) - 1)

    def ksa(self) -> None:
        for i in range(32):
            self.keys.append(self.rotate_left(i) ^ 0xabcdef)


if __name__ == '__main__':
    schiffy: Schiffy128 = Schiffy128()
    print(hex(schiffy.keys[31]))