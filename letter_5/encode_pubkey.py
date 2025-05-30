import base64
import re
from typing import Tuple, Dict


class KeyEncoder:
    def __init__(self, key_string: str) -> None:
        self._key_string: str = key_string

    def _clean_and_decode_key(self) -> bytes:
        """
        Entferne und decodiere den öffentlichen Schlüssel
        :return:
        """
        encoded_key: str = re.sub(r"-----.*?-----|\s", "", self._key_string)
        return base64.b64decode(encoded_key)

    def _read_length(self, data: bytes, offset: int) -> Tuple[int, int]:
        """
        Dem PublicKey liegt dem Abstract Syntax Notation zugrunde, welche aus dem Tag, der Länge und dem eigentlichen
        Wert besteht. Diese müssen gefiltert werden und extrahiert werden, um so den öffentlichen Schlüssel zu bekommen.

        Diese Methode liest die Länge des ASN.1 aus, welche in der kurz oder lanform vorliegen kann, die ab dem offset abgelesen wird.
        :param data:
        :param offset:
        :return:
        """
        length: int = data[offset]
        offset += 1
        if length & 0x80:  # Lange Form
            number_bytes: int = length & 0x7F
            length = int.from_bytes(data[offset:offset + number_bytes], "big")
            offset += number_bytes
        return length, offset

    def _read_sequence(self, data: bytes, offset: int) -> Tuple[int, int]:
        """
        Hier wird das Tag gelesen
        :param data:
        :param offset:
        :return:
        """
        return self._read_length(data, offset + 1)

    def _skip_algorithm_identifier(self, data: bytes, offset: int) -> int:
        """
        Hier wird der Algorithmus Identifier übersprungen.
        :param data:
        :param offset:
        :return:
        """
        length, offset = self._read_sequence(data, offset)
        offset += 13
        return offset

    def _read_bit_string(self, data: bytes, offset: int) -> int:
        """
        Hier beginnt der eigentliche bit stream, welcher den jeweiligen modulus und den öffentlichen Exponenten enthält
        :param data:
        :param offset:
        :return:
        """
        length, offset = self._read_length(data, offset + 1)
        return offset + 1

    def _read_integer(self, data: bytes, offset: int) -> Tuple[int, int]:
        """
        Da die vorherigen Methoden dazu zuständig waren, den ANS.1 zu überspringen, kann ab dem neuen offset, welcher
        immer erhöht wurde gelesen werden.
        :param data:
        :param offset:
        :return:
        """
        length, offset = self._read_length(data, offset + 1)
        integer_value = int.from_bytes(data[offset:offset + length], "big")
        offset += length
        return integer_value, offset

    def get_pub_key(self) -> Dict[str, int]:
        """
        Hier wird dann schließlich der Öffentliche Exponent und der Modulus getrennt und hier laufen alle zusammen
        :return:
        """
        data: bytes = self._clean_and_decode_key()
        offset: int = 0 # Starte bei index 0

        # Skip ANS 1 Struktur
        length, offset = self._read_sequence(data, offset) # Lese die Sequenz ein
        offset = self._skip_algorithm_identifier(data, offset) # Überspringe ANS 1 und bekomme neuen Index
        offset = self._read_bit_string(data, offset) # lese den Bit String aus
        length, offset = self._read_sequence(data, offset) # Bekomme neue Länge des RSA Schlüssels

        modulus, offset = self._read_integer(data, offset) # Lese ab dem Offset den Modulus ab
        exponent, offset = self._read_integer(data, offset) # Lese ab dem Offset den exponenten ab

        return (modulus, exponent)


if __name__ == "__main__":
    with open("pubkey.txt", "r") as f:
        key_data: str = f.read()
    # Der öffentliche Exponent und der Modulus wird extrahiert
    ke = KeyEncoder(key_data)
    pub_key: Dict[str, int] = ke.get_pub_key()
    print(pub_key)
