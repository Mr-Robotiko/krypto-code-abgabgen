import random
import string
from typing import Tuple, List

from authentification_function import AuthenticationFunction


class ExtensionAttack(AuthenticationFunction):
    def __init__(self, known_mac: Tuple, key_length: int = 16):
        super().__init__()
        self.key_length: int = key_length
        self.known_mac: Tuple[bytes, int] = known_mac

    def generate_random_extension(self, length: int = 6) -> bytes:
        '''
        Generiere eine zufällig Extension für den Angriff mit der Länge 6
        :param length:
        :return:
        '''
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length)).encode("utf-8")

    def pad_message(self, total_len: int) -> bytes:
        '''
        Berechnet die Padding Länge für die gegebene Nachricht und gibt die Anzahl der 0xff zurück,
        um die vollen vier Bytes aufzufüllen
        :param total_len:
        :return:
        '''
        pad_len: int = (4 - (total_len % 4))
        return b'\xff' * pad_len

    def to_block(self, data: bytes) -> list[int]:
        '''
        Erzeugt auf Basis der Extension die dazugehörigen Blöcke und vervollständigt diese
        :param data:
        :return:
        '''
        blocks = list()
        i: int = 0
        while i + 4 <= len(data): # Alle vier Byte Blöcke werden direkt umgewandelt
            blocks.append(int.from_bytes(data[i:i + 4], byteorder='big'))
            i += 4
        if i < len(data): # Alle Bytes, die übrig bleiben, werden mit 0xff aufgegüllt
            remaining: bytes = data[i:]
            pad: bytes = remaining + b'\xff' * (4 - len(remaining))
            blocks.append(int.from_bytes(pad, byteorder='big'))
        return blocks

    def attack(self):
        known_msg, known_mac = self.known_mac
        extension: bytes = self.generate_random_extension()

        original_len: int = self.key_length + len(known_msg)
        padded_msg: bytes = known_msg + self.pad_message(original_len) # Padding wird an der Nachricht angehangen
        new_message: bytes = padded_msg + extension # m || padding || extension

        # Berechnet die MIC auf Basis der zuvor durchgeführten Manipulation
        state: int = known_mac
        for block in self.to_block(extension):
            state = self.update(state, block)

        new_mac: int = self.Q(state)

        print("=== Extension-Angriff ===")
        print(f"Benutzte bekannte Nachricht:  {known_msg}")
        print(f"Bekannter MIC:                {hex(known_mac)}")
        print(f"Erzeugte Extension:           {extension}")
        print(f"Gefälschte Nachricht:         {new_message}")
        print(f"Neuer gültiger MIC:           {hex(new_mac)}\n")
        return new_message, new_mac


if __name__ == "__main__":
    attack_sequence: List[ExtensionAttack] = list()

    attack1 = ExtensionAttack((b'abcd', 0x632e4e5c))
    attack_sequence.append(attack1)
    attack2 = ExtensionAttack((b'abcdef', 0x0f6b8802))
    attack_sequence.append(attack2)
    attack3 = ExtensionAttack((b'abcdefghijk', 0x2638a819))
    attack_sequence.append(attack3)
    attack4 = ExtensionAttack((b'foobar', 0x782a826e))
    attack_sequence.append(attack4)
    attack5 = ExtensionAttack((b'barfoo', 0x885dc316))
    attack_sequence.append(attack5)

    for i in range(len(attack_sequence)):
        attack_sequence[i].attack()
