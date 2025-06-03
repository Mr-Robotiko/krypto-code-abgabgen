class Asn1:
    @staticmethod
    def encode_integer(x: int) -> bytes:
        b: bytes = x.to_bytes((x.bit_length() + 7) // 8 or 1, 'big')
        if b[0] & 0x80:
            b = b'\x00' + b
        return b'\x02' + bytes([len(b)]) + b

    @staticmethod
    def encode_ecdsa_signature(sig) -> bytes:
        r_enc = Asn1.encode_integer(sig.r)
        s_enc = Asn1.encode_integer(sig.s)
        seq = r_enc + s_enc
        return b'\x30' + bytes([len(seq)]) + seq
