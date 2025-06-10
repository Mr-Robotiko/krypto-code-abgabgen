from parameter_initializer import Initializer
from curve import EllipticCurve
from ec_point import ECPoint
from ecdsa import ECDSASigner
from asn1 import ASN1


def read_message(path: str = "data/message.txt") -> bytes:
    with open(path, "r") as f:
        message: str = f.read()
    return message.encode("utf-8")


def main():
    encoder: ASN1 = ASN1()
    init: Initializer = Initializer()
    curve: EllipticCurve = EllipticCurve(**init.curve_param)
    private_key: int = init.key_param["priv"]
    m_byte = read_message()  # Nicht wundern, ist verschlüsselt und codiert.
    signer: ECDSASigner = ECDSASigner()
    signature = signer.get_sig(curve, private_key, m_byte)
    sig_encoded = encoder.encode_sig(signature)

    with open("message.bin", "wb") as f:
        # OpenSSL will die Nachricht irgendwie nicht verifizieren.
        # Komme nicht darauf warum
        f.write(m_byte)

    with open("sig.bin", "wb") as f:
        # OpenSSL will die Nachricht irgendwie nicht verifizieren.
        # Komme nicht darauf warum
        f.write(sig_encoded)


if __name__ == "__main__":
    main()


