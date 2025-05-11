from bes_field import BESField


def task_1(a: int = 0x7b, b: int = 0xab):
    a: int = BESField(a) # x^6 + x^5 + x^4 + x^3 + x +1
    b: int = BESField(b) # x^7 + x^5 + x^3 + x + 1

    product: int = a * b
    print(f"{a} * {b} = {product}")

    inv: int = a.inverse()
    check: int = a * inv
    print(f"Inverse of {a} is {inv}, check: {check}")


def main():
    task_1()


if __name__ == '__main__':
    main()
