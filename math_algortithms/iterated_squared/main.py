def square_and_multiply(base: int, exponent: int, mod: int) -> int:
    if exponent == 0:
        return 1

    if exponent % 2 == 0:
        half = square_and_multiply(base, exponent // 2, mod)
        return (half * half) % mod

    else:
        return (base * square_and_multiply(base, exponent - 1, mod)) % mod


def main():
    check: bool = True
    while check:
        basis: int = int(input("Was ist die Basis:\t"))
        power: int = int(input("Was ist die Potenz:\t"))
        mod: int = int(input("Was ist das Modulo:\t"))

        print(f"Löse: {basis}^{power} = x mod {mod}\t")
        x: int = square_and_multiply(basis, power, mod)

        print(f"{basis}^{power} = {x} mod {mod}")


if __name__ == '__main__':
    main()
