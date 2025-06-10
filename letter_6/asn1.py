from typing import Tuple


class ASN1:
    '''
    https://datatracker.ietf.org/doc/html/rfc3279#section-2.2.3
     Ecdsa-Sig-Value  ::=  SEQUENCE  {
           r     INTEGER,
           s     INTEGER  }
    '''

    def encode_int(self, x: int) -> bytes:
        b = x.to_bytes((x.bit_length() + 7) // 8 or 1, 'big')  # fallback für 0
        if b[0] & 0x80:
            b = b'\x00' + b
        return b'\x02' + len(b).to_bytes(1, 'big') + b

    def encode_sig(self, sig: Tuple[int, int]) -> bytes:
        encoded_r: bytes = self.encode_int(sig[0])  # r
        encoded_s: bytes = self.encode_int(sig[1])  # s
        sequence = encoded_r + encoded_s
        encoded_sig = b"\x30" + len(sequence).to_bytes(1, byteorder = "big") + sequence
        return encoded_sig
