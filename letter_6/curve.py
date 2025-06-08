from ec_point import ECPoint


class EllipticCurve:
    def __init__(self, **values):
        self.a: int = values["a"]
        self.b: int = values["b"]
        self.p: int = values["p"]
        self.n: int = values["n"]
        self.G = ECPoint(values["gx"], values["gy"], self)

    def inverse(self, x: int) -> int:
        return pow(x, -1, self.p)  # x^-1 = 1 mod p
