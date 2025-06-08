import hashlib
import random

from curve import EllipticCurve
from ec_point import ECPoint


class ECDSASigner:

    @staticmethod
    def get_sig(curve: EllipticCurve, d: int, m: bytes):
        e: str = hashlib.sha256(m).hexdigest()
        e_int: int = int(e, 16)
        k: int = random.randint(1, curve.n)
        R: ECPoint = k * curve.G
        k_inv: int = pow(k, -1, curve.n)
        s: int = ((e_int + (R.x * d)) * k_inv) % curve.n

        return s, R.x

