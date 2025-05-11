class BESField:
    BES_POLYNOMIAL: int = 0x1C3

    def __init__(self, value: int):
        self.value = value & 0xFF

    def __repr__(self):
        return f"BESField(0x{self.value:02x})"

    def __add__(self, other):
        return BESField(self.value ^ other.value)

    def __mul__(self, other):
        a: int = self.value
        b: int = other.value
        result: int = 0
        for _ in range(8):
            if b & 1:
                result ^= a
            msb: int = a & 0x80
            a = (a << 1) & 0xFF
            if msb:
                a ^= BESField.BES_POLYNOMIAL & 0xFF
            b >>= 1
        return BESField(result)

    def get_value(self):
        return self.value

    def inverse(self):
        for i in range(1, 256):
            if (self * BESField(i)).get_value() == 1:
                return BESField(i)
