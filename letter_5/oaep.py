import hashlib as h
import os

class Oaep:
    def __init__(self, message: str, n: int, e: int, rsa_key_length: int = 1024):
        '''
        Definition der Standartparameter
        :param message:
        :param n:
        :param e:
        :param rsa_key_length:
        '''
        self.hash_function = h.sha1
        self.rsa_key_length: int = rsa_key_length // 8
        self.hash_output_length: int = self.hash_function().digest_size
        self.message_bytes: bytes = message.encode("utf-8")
        self.n: int = n
        self.e: int = e
        self.seed: bytes = os.urandom(self.hash_output_length)

    def mgf1(self, seed: bytes, length: int) -> bytes:
        '''
        Wikipedia: https://en.wikipedia.org/wiki/Mask_generation_function
        :param seed:
        :param length:
        :return:
        '''
        hash_output_length: int = h.sha256().digest_size
        if length > (hash_output_length << 32):
            raise ValueError("mask too long")
        T = b""
        counter = 0
        while len(T) < length:
            C = counter.to_bytes(4, 'big')
            T += h.sha256(seed + C).digest()
            counter += 1
        return T[:length]

    def encode_message(self) -> bytes:
        '''
        Encoden der Nachricht mit mgf und hinzufügen des Paddings
        :return:
        '''
        message_length: int = len(self.message_bytes)
        message_hash: bytes = self.hash_function(self.message_bytes).digest()
        padding_length: int = self.rsa_key_length - message_length - 2*self.hash_output_length - 2 # Formel aus Wikipedia

        # Bauen das Datenblocks
        padding: bytes = b"\x00" * padding_length
        data_block: bytes = message_hash + padding + b"\x01" + self.message_bytes  # Datenblock
        seed: bytes = self.seed

        msk_db: bytes = self.mgf1(seed, len(data_block))
        masked_db: bytes = bytes(x ^ y for x, y in zip(data_block, msk_db))

        msk_seed: bytes = self.mgf1(masked_db, len(seed))
        masked_seed: bytes = bytes(x ^ y for x, y in zip(seed, msk_seed))

        encoded_message: bytes = b"\x00" + masked_seed + masked_db # Finale maskierte Nachricht
        return encoded_message

    def rsa_encrypt(self) -> bytes:
        '''
        Verschlüsseln der encodeten Nachricht
        :return:
        '''
        encoded_message: bytes = self.encode_message()
        print("Encoded message (OAEP padded):", encoded_message)
        plaintext: int = int.from_bytes(encoded_message, "big")
        ciphertext = pow(plaintext, self.e, self.n)
        ciphertext_bytes = ciphertext.to_bytes(self.rsa_key_length, "big")
        print("Ciphertext (RSA encrypted):", ciphertext_bytes)
        return ciphertext_bytes

    def write_out(self, filename="ciphertext.bin"):
        '''
        Schreiben der Binärdatei
        :param filename:
        :return:
        '''
        ciphertext: bytes = self.rsa_encrypt()
        with open(filename, "wb") as f:
            f.write(ciphertext)


if __name__ == '__main__':
    from encode_pubkey import KeyEncoder

    with open("pubkey.txt", "r") as f:
        key_data = f.read()

    ke = KeyEncoder(key_data)
    n, e = ke.get_pub_key()
    # Der Schlüssel in pubkey.txt ist der öffentliche Schlüssel von Claas Wenk. Nicht ihrer.
    oaep = Oaep("Hypercube am Morgen vertreibt Kummer und Sorgen! Dafür muss man gesund für sein!", n, e, 1024)
    oaep.write_out()
