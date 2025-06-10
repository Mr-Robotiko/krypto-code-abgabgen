import hashlib
import secrets

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

