import hashlib
from .elliptic_curve import EllipticCurve
from .ecdsa import EcdsaSignature


def ecdsa_sign(d: int, m: int, k: int, curve: EllipticCurve) -> EcdsaSignature:
    R = k * curve.G
    r = R.x % curve.n
    k_inv = pow(k, -1, curve.n)
    s = (k_inv * (m + r * d)) % curve.n
    return EcdsaSignature(r, s)


def recover_private_key(m1, r, s1, m2, s2, n):
    if s1 == s2:
        raise ValueError("Fehler: Signaturen haben gleiches s, aber unterschiedliche m.")
    k = ((m1 - m2) * pow(s1 - s2, -1, n)) % n
    d = ((s1 * k - m1) * pow(r, -1, n)) % n
    return d


if __name__ == "__main__":
    # P-256 Parameters
    p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
    a = -3
    b = int("5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B", 16)
    gx = int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16)
    gy = int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16)
    n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

    curve = EllipticCurve(a, b, p, n, gx, gy)

    d = 0xdeadbeef1234567890abcdef
    k = 0x123456789abcdef123456789

    m1 = int.from_bytes(hashlib.sha256(b"Message One").digest(), 'big')
    m2 = int.from_bytes(hashlib.sha256(b"Message Two").digest(), 'big')

    sig1 = ecdsa_sign(d, m1, k, curve)
    sig2 = ecdsa_sign(d, m2, k, curve)

    with open("message1.bin", "wb") as f:
        f.write(m1.to_bytes(32, 'big'))
    with open("message2.bin", "wb") as f:
        f.write(m2.to_bytes(32, 'big'))
    with open("signature1.bin", "wb") as f:
        f.write(sig1.to_der())
    with open("signature2.bin", "wb") as f:
        f.write(sig2.to_der())

    d_rec = recover_private_key(m1, sig1.r, sig1.s, m2, sig2.s, curve.n)

    print(f"Original d:   {hex(d)}")
    print(f"Recovered d:  {hex(d_rec)}")
    assert d == d_rec
