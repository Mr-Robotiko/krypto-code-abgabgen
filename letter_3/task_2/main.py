from random import randbytes
from schiffy128 import Schiffy128

class Schiffy128CBC(Schiffy128):
    def __init__(self, message: str):
        # Initalisiere Schiffy128 mit den Schlüssel Q. Encode die Nachricht und füge Padding hinzu -> vielfaches von 16 Bytes
        super().__init__(inital_key=0x08150000000000000000000000004711)
        self.message_bytes: bytes = message.encode("utf-8")
        self.__add_padding()

        # Erstelle randomisierten IV und füge ihn den Ciphertext hinzu. Setze ihn als start Block für CBC
        self.iv: int = int.from_bytes(randbytes(16), byteorder="big")
        self.ciphertext: bytes = self.iv.to_bytes(16, "big")
        self.previous_block: int = self.iv

        # Verschlüssle die Nachricht und schreibe die Binary-Datei
        self.__encrypt()
        self.__write_out()

    def __add_padding(self) -> None:
        '''
        Fügt das Padding an die Nachricht hinzu, um ein vielfaches von 16 Bytes zu erreichen
        :return:
        '''
        padding_length: int = 16 - (len(self.message_bytes) % 16)
        self.message_bytes += bytes([padding_length] * padding_length)

    def __encrypt(self) -> None:
        '''
        Verschlüssle die Nachricht. Jeder Block wird mit dem vorherigen verxored. Es sind immer
        16 Byte Blöcke. Also IV XOR ersten Block. Ergebnis XOR zweiter Block ...
        Das verschlüsselte Ergebniss wird dem Ciphertext angehangen. Der vorherige Block wird
        zum Verschlüsseltem Block.
        :return:
        '''
        for i in range(0, len(self.message_bytes), 16):
            block: int = int.from_bytes(self.message_bytes[i:i+16], 'big')
            block_xored_previous: int = block ^ self.previous_block
            encrypted_block: int = self.E(block_xored_previous)
            self.ciphertext += encrypted_block.to_bytes(16, "big")
            self.previous_block = encrypted_block

    def __write_out(self) -> None:
        '''
        Schreibe die Binary-Datei
        :return:
        '''
        with open('ciphertext.bin', 'wb') as f:
            f.write(self.ciphertext)


if __name__ == '__main__':
    test = Schiffy128CBC("https://tinyurl.com/4h6tbznj") # Hier die Nachricht
