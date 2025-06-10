from typing import Tuple


class ASN1:
    '''
    https://datatracker.ietf.org/doc/html/rfc3279#section-2.2.3
     Ecdsa-Sig-Value  ::=  SEQUENCE  {
           r     INTEGER,
           s     INTEGER  }
    '''

    def encode_int(self, x: int) -> bytes:
        '''
        Defines how to encode an integer in asn 1
        :param x:
        :return:
        '''
        b = x.to_bytes((x.bit_length() + 7) // 8 or 1, 'big')  # fallback für 0
        if b[0] & 0x80:
            b = b'\x00' + b
        return b'\x02' + len(b).to_bytes(1, 'big') + b

    def encode_sig(self, sig: Tuple[int, int]) -> bytes:
        '''
        Encodes the whole signature
        :param sig:
        :return:
        '''
        encoded_r: bytes = self.encode_int(sig[0])  # r
        encoded_s: bytes = self.encode_int(sig[1])  # s
        sequence = encoded_r + encoded_s
        encoded_sig = b"\x30" + len(sequence).to_bytes(1, byteorder = "big") + sequence
        return encoded_sig

    def decode_sig(self, data: bytes) -> Tuple[int, int]:
        '''
        Decodes the whole signature
        :param data:
        :return:
        '''
        pos: int = 2
        r_len: int = data[pos + 1]
        r_bytes: bytes = data[pos + 2: pos + 2 + r_len]
        r: int = int.from_bytes(r_bytes, 'big')
        pos = pos + 2 + r_len
        s_len: int = data[pos + 1]
        s_bytes: bytes = data[pos + 2: pos + 2 + s_len]
        s: int = int.from_bytes(s_bytes, 'big')
        return r, s
