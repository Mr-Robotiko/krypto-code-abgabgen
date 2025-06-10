import hashlib
import secrets
from typing import Tuple

from curve import EllipticCurve
from ec_point import ECPoint


class ECDSASigner:

    @staticmethod
    def get_sig(curve: EllipticCurve, d: int, m: bytes):
        e: int = int(hashlib.sha256(m).hexdigest(), 16)
        k: int = secrets.randbelow(curve.n - 1)
        R: ECPoint = k * curve.G
        r: int = R.x % curve.n
        k_inv: int = pow(k, -1, curve.n)
        s: int = (k_inv * (e + r * d)) % curve.n
        return r, s

    @staticmethod
    def recover_private_key(curve: EllipticCurve, m1: bytes, sig1: Tuple[int,int], m2: bytes, sig2: Tuple[int,int]) -> int:
        r1, s1 = sig1
        r2, s2 = sig2
        e1: int = int(hashlib.sha256(m1).hexdigest(), 16)
        e2: int = int(hashlib.sha256(m2).hexdigest(), 16)

        numerator: int = (e2 * s1 - e1 * s2) % curve.n
        denominator: int = (r1 * (s2 - s1)) % curve.n
        denominator_inv: int = pow(denominator, -1, curve.n)
        d: int = (numerator * denominator_inv) % curve.n
        return d

