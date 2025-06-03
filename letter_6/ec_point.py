from __future__ import annotations


class ECPoint:
    def __init__(self, x: int, y: int, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def __neg__(self) -> ECPoint:
        return ECPoint(self.x, (-self.y) % self.curve.p, self.curve)

    def __add__(self, other: ECPoint) -> ECPoint:
        # Unendlichkeitsbehandlung
        if self.x is None or self.y is None:
            return other
        if other.x is None or other.y is None:
            return self

        if self == other:
            # Punktverdopplung
            if self.y == 0:
                return self.curve.infinity()
            m = ((3 * self.x ** 2 + self.curve.a) *
                 self.curve.inverse(2 * self.y)) % self.curve.p
        elif self.x == other.x:
            return self.curve.infinity()  # P + (-P) = ∞
        else:
            # Punktaddition
            m = ((other.y - self.y) *
                 self.curve.inverse(other.x - self.x)) % self.curve.p

        x_r = (m * m - self.x - other.x) % self.curve.p
        y_r = (m * (self.x - x_r) - self.y) % self.curve.p

        return ECPoint(x_r, y_r, self.curve)

    def __rmul__(self, k: int) -> ECPoint:
        result = self.curve.infinity()
        addend = self

        while k:
            if k & 1:
                result = result + addend
            addend = addend + addend
            k >>= 1
        return result

    def __repr__(self):
        return f"({self.x}, {self.y})"
