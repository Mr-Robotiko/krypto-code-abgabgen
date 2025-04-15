
def iterated_squares(basis: int, power: int, mod: int):
    binary_power: bin = bin(power)[2:]
    x: int = basis
    for i in range(len(binary_power)):
        y: int = x**2 % mod
        if binary_power[i] == 0:
            x = y
        else:
            x = y * basis % mod
    print(f"{basis}^{power} = {x} mod {mod}")


def main():
    check: bool = True
    while check:
        basis: int = int(input("Was ist die Basis:\t"))
        power: int = int(input("Was ist die Potenz:\t"))
        mod: int = int(input("Was ist das modulo:\t"))

        print(f"Löse: {basis}^{power} = x mod {mod}\t")
        iterated_squares(basis, power, mod)


if __name__ == '__main__':
    main()
