def square_and_multiply(base: int, power: int, mod: int) -> int:
    if power == 0:
        return 1
    if power % 2 == 0: # b_n = 0
        x: int = square_and_multiply(base, power // 2, mod)
        return (x * x) % mod
    else:   # b_n = 1
        return (base * square_and_multiply(base, power - 1, mod)) % mod


def main():
    check: bool = True
    while check:
        base: int = int(input("Was ist die Basis:\t"))
        power: int = int(input("Was ist die Potenz:\t"))
        mod: int = int(input("Was ist das Modulo:\t"))

        print(f"Löse: {base}^{power} = x mod {mod}\t")
        x: int = square_and_multiply(base, power, mod)

        print(f"{base}^{power} = {x} mod {mod}")


if __name__ == '__main__':
    main()
