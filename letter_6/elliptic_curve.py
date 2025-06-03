from .ec_point import ECPoint


class EllipticCurve:
    def __init__(self, a: int, b: int, p: int, n: int, Gx: int, Gy: int):
        self.a = a
        self.b = b
        self.p = p
        self.n = n
        self.G = ECPoint(Gx, Gy, self)

    def inverse(self, x: int) -> int:
        return pow(x, -1, self.p)

    def infinity(self) -> ECPoint:
        return ECPoint(None, None, self)
