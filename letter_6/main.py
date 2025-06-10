from typing import Dict

from parameter_initializer import Initializer
from curve import EllipticCurve
from ecdsa import ECDSASigner
from asn1 import ASN1
import os


def read_message(path: str = "data/message.txt") -> bytes:
    with open(path, "r") as f:
        message: str = f.read()
    return message.encode("utf-8")


def read_file(path: str) -> bytes:
    file_directory = os.open(path, 0)
    try:
        size = os.stat(file_directory).st_size
        content = os.read(file_directory, size)
    finally:
        os.close(file_directory)
    return content


def attack(encoder: ASN1, curve: EllipticCurve):
    m1 = read_file("packages/1/message1.bin")
    m2 = read_file("packages/1/message2.bin")
    sig1_bytes = read_file("packages/1/signature1.bin")
    sig2_bytes = read_file("packages/1/signature2.bin")

    # Signaturen dekodieren
    sig1 = encoder.decode_sig(sig1_bytes)
    sig2 = encoder.decode_sig(sig2_bytes)

    # Privaten Schlüssel rekonstruieren
    d = ECDSASigner.recover_private_key(curve, m1, sig1, m2, sig2)

    # Privaten Schlüssel als Big-Endian bytes
    d_bytes = d.to_bytes((d.bit_length() + 7) // 8, "big")

    return d, d_bytes


def main():
    encoder: ASN1 = ASN1()
    init: Initializer = Initializer()
    curve: EllipticCurve = EllipticCurve(**init.curve_param)
    private_key: int = init.key_param["priv"]
    m_byte = read_message()  # Nicht wundern, ist verschlüsselt und codiert.
    signer: ECDSASigner = ECDSASigner()
    signature = signer.get_sig(curve, private_key, m_byte)
    sig_encoded = encoder.encode_sig(signature)
    print("=========== TASK 1 ===============")
    print(f"Signiture: {signature}")

    print("=========== TASK 2 ===============")
    print(f"Encoded: {sig_encoded}")

    with open("message.bin", "wb") as f:
        # OpenSSL will die Nachricht irgendwie nicht verifizieren.
        # Komme nicht darauf warum
        f.write(m_byte)

    with open("sig.bin", "wb") as f:
        # OpenSSL will die Nachricht irgendwie nicht verifizieren.
        # Komme nicht darauf warum
        f.write(sig_encoded)

    d, message = attack(encoder, curve)
    print("============ TASK 3 =================")
    print(f"Private Key: {d}\nMessage: {message}")


if __name__ == "__main__":
    main()
