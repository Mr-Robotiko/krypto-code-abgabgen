from typing import List, Tuple


class Schiffy128:

    def __init__(self):
        self.s0: int = 170
        self.inital_key: int = 0xdeadbeef000000000000000badc0ffee

        # blablabalabalo
        self.keys: List[int] = list()
        self.lookup_table: List[int] = list()
        self.split_blocks: List[int] = list()
        self.maped_blocks: List[str] = list()

        # Fill lookuptable and the round keys
        self.__s_box()
        self.__ksa()

    def __s_box(self) -> None:
        for x in range(256):
            self.lookup_table.append(170 if x == 0 else (37 * self.lookup_table[x-1] + 9) % 256)

    def __rotate_left(self, i: int) -> int:
        if i == 0:
            return self.inital_key
        else:
            return ((self.keys[i-1] << (7 * i) % 128) | (self.keys[i-1] >> (128 - (7 * i) % 128))) & ((1 << 128) - 1)

    def __ksa(self) -> None:
        for i in range(32):
            self.keys.append(self.__rotate_left(i) ^ 0xabcdef)

    def __cut_key(self, key: int) -> Tuple[int, int]:
        bin_key: bin = bin(key)[2:].zfill(128)
        msb_bin: bin = bin_key[:64]
        lsb_bin: bin = bin_key[64:]
        msb = int(msb_bin, 2)
        lsb = int(lsb_bin, 2)
        return msb, lsb

    def split(self, block_xor_msb: bin) -> None:
        self.split_blocks = []
        i = 0
        block_xor_msb: bin = block_xor_msb[2:]
        block_xor_msb = block_xor_msb.zfill(64)
        while i < len(block_xor_msb):
            byte_block: bin = block_xor_msb[i:i + 8]
            self.split_blocks.append(byte_block)
            i += 8

    def map_block_with_s_box(self):
        self.maped_blocks = []
        for block in self.split_blocks:
            list_block: List[str] = list(block)
            int_block: int = int(''.join(map(str, list_block)), 2)
            mapped_int_block: int = self.lookup_table[int_block]
            self.maped_blocks.append(bin(mapped_int_block))

    def merge(self) -> str:
        merged_bits: str = ""
        for mapped_block in self.maped_blocks:
            value: str = mapped_block.removeprefix("0b").zfill(8)
            merged_bits += value
        return merged_bits

    def F(self, block: int, k: int) -> int:
        msb, lsb = self.__cut_key(k)
        block_xor_msb: bin = bin(msb ^ block)

        self.split(block_xor_msb)
        self.map_block_with_s_box()
        merged_bits: str = self.merge()
        int_merged_bits: int = int(''.join(map(str, merged_bits)), 2)
        result: int = int_merged_bits ^ lsb

        return result


if __name__ == '__main__':
    schiffy: Schiffy128 = Schiffy128()
    test = schiffy.F(0x81f3d4d01743d570, schiffy.keys[30])
    print(hex(test))
