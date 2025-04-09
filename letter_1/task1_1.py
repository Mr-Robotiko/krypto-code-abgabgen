import hashlib as h


def H(value: str):
    hash = h.md5(value.encode("utf-8"))
    result = hash.hexdigest()[:10]
    print(result)


if __name__ == '__main__':
    H("")
    H("Leeroy Jenkins")
