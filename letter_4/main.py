from typing import List, Tuple

from bes_field import BESField


class BES:
    m: List[int] = [[0x59, 0x4c],
                    [0x4f, 0x4f]]

    def __init__(self, block: int):
        self.block: int = block
        self.s_box: List[int] = self.s_box()

    def s_box(self):
        '''
        Erstllt die S-Box von BES
        :return:
        '''
        s_box: List[int] = list()
        for i in range(256):
            a: BESField = BESField(i)  # x^6 + x^5 + x^4 + x^3 + x +1
            b: BESField = BESField(0xab)  # x^7 + x^5 + x^3 + x + 1
            product: int = a * b
            s_box.append(product)
        return s_box

    def split_block(self) -> Tuple[int]:
        '''
        Splitet den Eingabeblock in 4 Byte
        :return:
        '''
        b_0: int = (self.block >> 24) & 0xFF
        b_1: int = (self.block >> 16) & 0xFF
        b_2: int = (self.block >> 8) & 0xFF
        b_3: int = self.block & 0xFF
        return b_0, b_1, b_2, b_3

    def matrix_mul(self, ci: List[int]) -> List[BESField]:
        '''
        Führt eine Matrixmultiplikation durch
        :param ci: Spaltenvektor der Blockmatrix
        :return:
        '''
        column_result: List[BESField] = list()
        for row in BES.m:
            result = BESField(0)
            for a, b in zip(row, ci):
                result += BESField(a) * BESField(b)
            column_result.append(result)
        return column_result

    def mix_columns(self) -> Tuple[List[BESField]]:
        '''
        Führt die MixColumns Operation durch
        :return:
        '''
        input_blocks: Tuple[int] = self.split_block()
        c0: List[int] = input_blocks[:2]
        c1: List[int] = input_blocks[2:]

        result_c0: List[BESField] = self.matrix_mul(c0)
        result_c1: List[BESField] = self.matrix_mul(c1)

        return result_c0, result_c1


def main():
    '''
    Aufgabenspezifische Ausgabe
    :return:
    '''
    bes: BES = BES(0xa3caab05)
    s_123: BESField = bes.s_box[123]

    # Task 2: Inverse of 123:
    print("\nAufgabe 2: Fine das Inverse von S_123:")
    print("======================================")
    print(f"Das Element 123 der S-Box:\t{s_123}")
    print(f"Das inverse Element von 123 in F_256:\t{s_123.inverse()}")

    mc_0, m_c1 = bes.mix_columns()

    # Task 3: Calculate MixColumns
    print("\nAufgabe 3: Führe die Berechnung von 0xa3caab05 aus:")
    print("======================================")
    print(f"Mc_0 =\t{mc_0}\nMc_1 =\t{m_c1}")
    print("DEAD AFFE")


if __name__ == '__main__':
    main()