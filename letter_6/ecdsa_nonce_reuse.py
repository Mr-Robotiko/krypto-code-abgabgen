from typing import Tuple
from asn1 import ASN1
from curve import EllipticCurve
from ecdsa import ECDSASigner


class NonceAttack:
    def __init__(self, curve: EllipticCurve):
        self.curve: EllipticCurve = curve
        self.encoder: ASN1 = ASN1()
        self.signer: ECDSASigner = ECDSASigner()

    def sign_messages_with_reused_nonce(self, priv_key: int, nonce: int,
                                        m1: bytes, m2: bytes) -> Tuple[bytes, bytes]:
        sig1: Tuple[int, int] = self.signer.get_sig(self.curve, priv_key, m1, nonce)
        sig2: Tuple[int, int] = self.signer.get_sig(self.curve, priv_key, m2, nonce)
        sig1_enc: bytes = self.encoder.encode_sig(sig1)
        sig2_enc: bytes = self.encoder.encode_sig(sig2)
        return sig1_enc, sig2_enc

    def save_to_file(self, filename: str, data: bytes) -> None:
        with open(filename, "wb") as f:
            f.write(data)

    def save_message_files(self, m1: bytes, m2: bytes) -> None:
        self.save_to_file("message1.bin", m1)
        self.save_to_file("message2.bin", m2)

    def save_signature_files(self, sig1_enc: bytes, sig2_enc: bytes) -> None:
        self.save_to_file("signature1.bin", sig1_enc)
        self.save_to_file("signature2.bin", sig2_enc)

    def privkey_to_big_endian_message(self, priv_key: int, filename="private_key.bin"):
        priv_bytes: bytes = priv_key.to_bytes((priv_key.bit_length() + 7) // 8, "big")
        self.save_to_file(filename, priv_bytes)
