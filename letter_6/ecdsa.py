from dataclasses import dataclass
from .asn1 import Asn1


@dataclass
class EcdsaSignature:
    r: int
    s: int

    def to_der(self) -> bytes:
        return Asn1.encode_ecdsa_signature(self)
