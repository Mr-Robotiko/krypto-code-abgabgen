class BESField:
    BES_POLYNOMIAL: int = 0x1C3 # Das irreduzible Polynom {1c3}

    def __init__(self, value: int):
        '''
        Erstellen einer Klasse, die einen Wert im Feld 256 mit dem irreduziblen Polynom einordnet.
        Diese Datenstruktur nennt sich BES Feld und wird initalisiert für jeden einzelnen Wert.
        :param value:
        '''
        self.value: int = value

    def __repr__(self):
        '''
        Gibt die Werte des BES-Felds zurück in einer geeigneten Räpresentation
        :return: Den Wert als Hex-Wert
        '''
        return hex(self.value)

    def __add__(self, other):
        '''
        Beschreibt die Addition zweier Elemente per XOR
        :param other: Der zweite Summand, mit dem addiert wird.
        :return: Ergebnis der Addition
        '''
        return BESField(self.value ^ other.value)

    def __mul__(self, other):
        '''
        Definiert die Multiplikation in dem BES-Feld, welches dann durch das entsprechende irreduzible Polynom
        Reduziert wird.
        :param other: Der zweite Faktor mit dem das Produkt gebildet wird.
        :return: Das Produkt der Multiplikation
        '''
        a: int = self.value
        b: int = other.value
        result: int = 0
        for _ in range(8):
            if b & 1:
                result ^= a
            msb: int = a & 0x80
            a = (a << 1) & 0xFF
            if msb:
                a ^= BESField.BES_POLYNOMIAL & 0xFF
            b >>= 1
        return BESField(result)

    def get_BES_value(self) -> int:
        '''
        Gibt den Integerwert des BES-Felds zurück
        :return:
        '''
        return self.value

    def inverse(self):
        '''
        Brute-Force das inverse Element des BES-Feld Elements
        :return: Das inverse Element
        '''
        for i in range(1, 256):
            if (self * BESField(i)).get_BES_value() == 0x01:
                return BESField(i)