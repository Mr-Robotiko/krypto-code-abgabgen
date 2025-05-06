from typing import List, Tuple


class Schiffy128:

    def __init__(self, inital_key: int = 0xdeadbeef000000000000000badc0ffee):
        self.s0: int = 170
        self.inital_key: int = inital_key

        # Deklariere die wichtigen Arrays (Listen)
        self.keys: List[int] = list() # Sammlung der Schlüsseln
        self.lookup_table: List[int] = list() # S_Box
        self.split_blocks: List[int] = list() # 8 Bit Blöcke
        self.maped_blocks: List[str] = list() # S-Box mit den Blöcken

        # Fill lookuptable and the round keys
        self.__s_box() # Füllen des Lookup-Tables
        self.__ksa() # Füllen der KSA-Schlüssel

    def __s_box(self) -> None:
        '''
        Füllt die self.lookup_table auf mit den jeweiligen 8 x 8 Matrix
        :return:
        '''
        for x in range(256):
            self.lookup_table.append(170 if x == 0 else (37 * self.lookup_table[x-1] + 9) % 256)

    def __rotate_left(self, i: int) -> int:
        '''
        Die Rotation nach links für die Schlüsselerzeugung
        :param i:
        :return: rotierter Wert
        '''
        if i == 0:
            return self.inital_key
        else:
            return ((self.keys[i-1] << (7 * i) % 128) | (self.keys[i-1] >> (128 - (7 * i) % 128))) & ((1 << 128) - 1)

    def __ksa(self) -> None:
        '''
        Erzeugt die 32 Rundenschlüssel und füllt die self.keys damit auf.
        :return:
        '''
        for i in range(32):
            self.keys.append(self.__rotate_left(i) ^ 0xabcdef)

    def __cut_key(self, key: int) -> Tuple[int, int]:
        '''
        Unterteilt den Rundenschlüssel in MSB und LSB
        :param key:
        :return: Tuple von MSB und LSB
        '''
        bin_key: bin = bin(key)[2:].zfill(128)
        msb_bin: bin = bin_key[:64]
        lsb_bin: bin = bin_key[64:]
        msb = int(msb_bin, 2)
        lsb = int(lsb_bin, 2)
        return msb, lsb

    def __split(self, block_xor_msb: bin) -> None:
        '''
        Splitet den verxorten Block mit den MSB in jeweils 8 Bit Blöcke. Füllt die self.split_blocks auf
        :param block_xor_msb:
        :return:
        '''
        self.split_blocks = []
        i = 0
        block_xor_msb: bin = block_xor_msb[2:]
        block_xor_msb = block_xor_msb.zfill(64)
        while i < len(block_xor_msb):
            byte_block: bin = block_xor_msb[i:i + 8]
            self.split_blocks.append(byte_block)
            i += 8

    def __map_block_with_s_box(self) -> None:
        '''
        Substituiert die Werte der self.split_blocks mit den jeweiligen Indizies der S-Box Lookup-Table
        :return:
        '''
        self.maped_blocks = []
        for block in self.split_blocks:
            list_block: List[str] = list(block)
            int_block: int = int(''.join(map(str, list_block)), 2)
            mapped_int_block: int = self.lookup_table[int_block]
            self.maped_blocks.append(bin(mapped_int_block))

    def __merge(self) -> str:
        '''
        Fügt die substituierten Werte zusammen.
        :return: Den zusammengefügten Bitstream
        '''
        merged_bits: str = ""
        for mapped_block in self.maped_blocks:
            value: str = mapped_block.removeprefix("0b").zfill(8)
            merged_bits += value
        return merged_bits

    def F(self, block: int, k: int) -> int:
        '''
        Simuliert die Feistel-Funktion laut dem Übungsblatt. Der Schlüssel und der Block gehen in die Funktion rein und
        werden entsprechend der Definition verarbeitet.
        :param block:
        :param k:
        :return: Den finalen Bitstream
        '''
        msb, lsb = self.__cut_key(k)
        block_xor_msb: bin = bin(msb ^ block)

        self.__split(block_xor_msb)
        self.__map_block_with_s_box()
        merged_bits: str = self.__merge()
        int_merged_bits: int = int(''.join(map(str, merged_bits)), 2)
        result: int = int_merged_bits ^ lsb

        return result

    def E(self, block: int) -> int:
        '''
        Führt die 32 Runden durch und verschlüsselt den Block mit der Feistel Funktion.
        :param message:
        :return: Gibt den verschlüsselten Wert nach 32 Runden zurück
        '''
        left: int = (block >> 64) & ((1 << 64) - 1)  # linke Hälfte der Nachricht
        right: int = block & ((1 << 64) - 1)  # rechte Hälfte der Nachricht

        for key in self.keys:
            result_of_F: int = self.F(right, key)
            f_left = right
            f_right = left ^ result_of_F
            left, right = f_left, f_right

        # Führe am Ende die Hälften zusammen von Links und Rechts
        result: int = (left << 64) | right
        return result


if __name__ == '__main__':
    schiffy: Schiffy128 = Schiffy128()
    test = schiffy.E(0x0000000000000000)
    print(hex(test))
