from typing import List

from authentification_function import AuthenticationFunction


class ExtensionAttack(AuthenticationFunction):
    def __init__(self, known_mic: int, known_message: str, key_length: int = 16) -> None:
        super().__init__()
        self.known_mic: int = known_mic
        self.known_message: str = known_message
        self.key_length: int = key_length
        self.initial_state = self.recover_state()
        # Der letzte Zustand der MIC wird näherungsweise bestimmt und überschreibt den Initialzustand S_0
        # S_0 entspricht S_n (letzter Zustand von MIC)

    def generate_sn(self, start_bit) -> int:
        '''
        Generiere den internen Zustand sn basierend auf der MIC und dem Startbit.
        :param start_bit: Testet 0 und 1
        :return:
        '''
        bin_mic: bin = bin(self.known_mic)[2:].zfill(32)
        bitblock: List[int] = [start_bit] + [0] * 31
        i: int = 0
        for _ in range(32):
            next_index = (i + 17) % 32
            # Da es sich um eine Rotation handelt, ist es der Körper F_32, welcher Zyklich ist.
            # Dementsprechend wird immer um 17 Positionen gesprungen und differenziert nach 0 und 1
            if bin_mic[i] == "1":
                bitblock[next_index] = (bitblock[i] + 1) % 2
                # Wenn es eine 1 ist, so wird das Bit invertiert 0 -> 1, 1 -> 0
            else:
                bitblock[next_index] = bitblock[i]
                # Wenn es eine 0 ist, wird das Bit übernommen
            i = next_index # Fahre mit dem neuen Index fort
        sn_bin = ''.join(str(b) for b in bitblock)
        return int(sn_bin, 2)

    def recover_state(self) -> int:
        '''
        Versuche beide Startbits und berechne den Zustand sn näherungsweise.
        :return: Gefundener Zustand S_n
        '''
        candidates: List[int] = [self.generate_sn(0), self.generate_sn(1)]
        for c in candidates:
            if self.Q(c) == self.known_mic: # Prüft, ob einer der beiden der bekannten MIC entspricht.
                return c
        raise ValueError("Kein gültiger Zustand sn gefunden")

    def extension_attack(self, extension: str) -> int:
        '''
        Generiere den gefälschten MIC, indem die Erweiterung nach dem Padding verarbeitet wird.
        :param extension: Die Extension die angefügt werden soll.
        :return: den neuen MIC
        '''
        # Um die Nachricht der MIC zu manipulieren, muss der Padding der Originalnachricht berechnet werden
        original_len: int = self.key_length + len(self.known_message)
        padding_len: int = (4 - (original_len % 4)) % 4
        padding: bytes = b'\xff' * padding_len

        # Schließlich kann die Verarbeitung der Extension simuliert werden auf Basis des Padding
        ext_bytes: bytes = padding + extension.encode("utf-8")
        if len(ext_bytes) % 4 != 0:
            ext_bytes += b'\xff' * (4 - len(ext_bytes) % 4)

        i = 0
        # Zuletzt wird der Block mit dem letzten Zustand verarbeitet als wäre die Nachricht noch nicht final
        # Der berechnete Initalzustand am Anfang beinhaltet alle Zwischenschritte der Originalnachricht.
        while i < len(ext_bytes):
            block = int.from_bytes(ext_bytes[i:i + 4], byteorder="big")
            self.initial_state = self.update(self.initial_state, block)
            i += 4

        # Nun wird die gültige MIC erzeugt, die durch den Unittest validiert wird.
        return self.Q(self.initial_state)


def main() -> None:
    '''
    Hier können Sie eigene Extensions and die Nachricht "abcd" mit der MIC 0x632e4e5c anfügen.
    Sie können auch "ef" mit 0x0f6b8802 testen oder "efghijk" mit 0x2638a819 testen.
    Speziell gebe ich Ihnen die Nachricht "enigma" mit der MIC 0x5e535a7a.
    Unter test_task_2_2.py finden Sie auch die Unittests für die ersten beiden Testvektoren.
    :return: None
    '''
    while True:
        extension: str = input("Welche Nachricht soll angehangen werden? (ENTER für Verlassen)\t")
        if extension == "":
            break
        attack: ExtensionAttack = ExtensionAttack(0x632e4e5c, "abcd")
        fake_mic: int = attack.extension_attack(extension)
        print("Gefälschte Nachricht:", attack.known_message + extension)
        print("Gefälschter MIC:     ", hex(fake_mic))
        print("===============================================")


if __name__ == '__main__':
    main()
