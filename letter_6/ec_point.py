
class ECPoint:
    def __init__(self, x: int, y: int, curve):
        self.x: int = x
        self.y: int = y
        self.curve = curve

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.curve == other.curve

    def __rmul__(self, scalar: int):
        return self * scalar

    def __neg__(self):
        return ECPoint(self.x, (-self.y) % self.curve.p, self.curve)

    def __add__(self, other):
        # Q = (u.v)
        if other == self:  # P + P = 2 * P Double
            m: int = ((3 * (self.x**2) + self.curve.a) * self.curve.inverse(2 * self.y)) % self.curve.p  # (3*r^2+a) * (2*s)^-1
            u: int = (m**2 - 2 * self.x) % self.curve.p  # (m^2 - 2 * r) mod p
            v: int = (m * (u - self.x) + self.y) % self.curve.p  # m * (u - r) + s mod p
        else:  # A + B
            m: int = ((other.y - self.y) * self.curve.inverse(other.x - self.x)) % self.curve.p  # s2-s1 * (r2-r1)^-1 mod p
            u: int = (m ** 2 - self.x - other.x) % self.curve.p  # m^2 - r1 - r2 mod p
            v: int = (m * (u - self.x) + self.y) % self.curve.p  # m*(u-r1) + s1 mod p

        return ECPoint(u, -v % self.curve.p, self.curve)  # Q = (u, -v) mod p

    def __mul__(self, scalar: int):
        result = None
        addend = self

        while scalar > 0:
            if scalar & 1:
                result = addend if result is None else result + addend
            addend = addend + addend
            scalar >>= 1

        return result

    def __repr__(self):
        return f"({self.x}, {self.y})"
