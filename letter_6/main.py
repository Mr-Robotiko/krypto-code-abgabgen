import random
from typing import Dict

from parameter_initializer import Initializer
from curve import EllipticCurve
from ec_point import ECPoint
from ecdsa import ECDSASigner

def main():
    init: Initializer = Initializer()
    curve: EllipticCurve = EllipticCurve(**init.curve_param)
    private_key: int = init.key_param["priv"]
    random_skalar: int = random.randint(1, curve.n)
    print(random_skalar)
    r = random_skalar * curve.G
    pub_key = private_key * curve.G
    print(pub_key, r)
    m = "Hello".encode("utf-8")
    signer: ECDSASigner = ECDSASigner()
    signiture = signer.get_sig(curve, private_key, m)
    print(signiture)


if __name__ == "__main__":
    main()


