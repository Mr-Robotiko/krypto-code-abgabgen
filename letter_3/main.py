

class Schiffy128:

    def __init__(self):
        self.s0: int = 170

    def s_box(self, number: int = 0) -> int:
        for x in range(number + 1):
            self.s0 = 170 if x == 0 else (37 * self.s0 + 9) % 256


if __name__ == '__main__':
    schiffy: Schiffy128 = Schiffy128()
    s = schiffy.s_box(1)
    print(schiffy.s0)
