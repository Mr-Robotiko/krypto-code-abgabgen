import os
import secrets
from typing import Tuple

from parameter_initializer import Initializer
from curve import EllipticCurve
from ecdsa import ECDSASigner
from asn1 import ASN1
from ecdsa_nonce_reuse import NonceAttack


def read_message(path: str = "data/message.txt") -> bytes:
    '''
    Reads message for task 2 which then will create a signature
    :param path:
    :return:
    '''
    with open(path, "r") as f:
        message: str = f.read()
    return message.encode("utf-8")


def read_file(path: str) -> bytes:
    '''
    Reads the file within the packages directory containing all enclosed files
    :param path:
    :return:
    '''
    file_directory = os.open(path, 0)
    try:
        size = os.stat(file_directory).st_size
        content = os.read(file_directory, size)
    finally:
        os.close(file_directory)
    return content


def calculate_d(encoder: ASN1, curve: EllipticCurve, package: str):
    '''
    Recovers the private key within the given messages which uses both the same nonce for task 3
    :param encoder:
    :param curve:
    :param package:
    :return:
    '''
    m1: bytes = read_file(f"packages/{package}/message1.bin")
    m2: bytes = read_file(f"packages/{package}/message2.bin")
    sig1_bytes: bytes = read_file(f"packages/{package}/signature1.bin")
    sig2_bytes: bytes = read_file(f"packages/{package}/signature2.bin")
    sig1: Tuple[int, int] = encoder.decode_sig(sig1_bytes)
    sig2: Tuple[int, int] = encoder.decode_sig(sig2_bytes)
    d: int = ECDSASigner.recover_private_key(curve, m1, sig1, m2, sig2)
    d_bytes: bytes = d.to_bytes((d.bit_length() + 7) // 8, "big")
    return d, d_bytes


def nonce_attack(priv_key: int, curve: EllipticCurve, nonce: int = 42):
    '''
    Creates two messages and the according signature for task 4
    :param priv_key:
    :param curve:
    :param nonce:
    :return:
    '''
    attack = NonceAttack(curve)

    m1 = b"https://tinyurl.com/5n7zfxyh"
    m2 = b"https://tinyurl.com/2rf8dafp"

    attack.save_message_files(m1, m2)
    sig1_enc, sig2_enc = attack.sign_messages_with_reused_nonce(priv_key, nonce, m1, m2)
    attack.save_signature_files(sig1_enc, sig2_enc)
    attack.privkey_to_big_endian_message(priv_key)


def main():
    encoder: ASN1 = ASN1()
    init: Initializer = Initializer()
    curve: EllipticCurve = EllipticCurve(**init.curve_param)
    private_key: int = init.key_param["priv"]
    m_byte = read_message()  # Nicht wundern, ist verschlüsselt und codiert. Task 2
    signer: ECDSASigner = ECDSASigner()
    k: int = secrets.randbelow(curve.n - 1)
    signature = signer.get_sig(curve, private_key, m_byte, k)
    sig_encoded = encoder.encode_sig(signature)

    print("=========== TASK 1 ===============")
    print(f"Signiture: {signature}")

    print("=========== TASK 2 ===============")
    print(f"Encoded: {sig_encoded}")

    with open("message.bin", "wb") as f:
        # OpenSSL will die Nachricht irgendwie nicht verifizieren.
        # Komme nicht darauf warum
        f.write(m_byte)

    with open("signature.bin", "wb") as f:
        # OpenSSL will die Nachricht irgendwie nicht verifizieren.
        # Komme nicht darauf warum
        f.write(sig_encoded)

    d1, message1 = calculate_d(encoder, curve, "1")
    d2, message2 = calculate_d(encoder, curve, "2")
    print("============ TASK 3 =================")
    print(f"Private Key: {d1}\nMessage: {message1}")
    print(f"Private Key: {d2}\nMessage: {message2}")

    nonce_attack(private_key, curve)


if __name__ == "__main__":
    main()
