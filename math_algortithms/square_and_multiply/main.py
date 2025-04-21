def square_and_multiply(base: int, power: int, mod: int, depth=0) -> int:
    indent = "  " * depth

    if power == 0:
        return 1

    if power % 2 == 0:
        print(f"{indent}power = {power} (gerade) → rechne ({base}^{power // 2})² mod {mod}")
        x = square_and_multiply(base, power // 2, mod, depth + 1)
        result = (x * x) % mod
        print(f"{indent}→ ({x}²) mod {mod} = {result}")
        return result
    else:
        print(f"{indent}power = {power} (ungerade) → rechne {base} * ({base}^{power - 1}) mod {mod}")
        result = (base * square_and_multiply(base, power - 1, mod, depth + 1)) % mod
        print(f"{indent}→ {base} * a^{power - 1} mod {mod} = {result}")
        return result


def main():
    while True:
        base: int = int(input("Was ist die Basis:\t"))
        power: int = int(input("Was ist die Potenz:\t"))
        mod: int = int(input("Was ist das Modulo:\t"))

        print(f"Löse: {base}^{power} = x mod {mod}\t")
        x: int = square_and_multiply(base, power, mod)

        print(f"{base}^{power} = {x} mod {mod}")
        print(f"{x = }")


if __name__ == '__main__':
    main()
