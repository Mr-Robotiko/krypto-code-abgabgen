import hashlib as h
import random
import string
import time


def H(value: str) -> str:
    hash = h.md5(value.encode("utf-8"))
    result = hash.hexdigest()[:10]
    return result


def attack():
    name: str = "RaphaelTack"
    attempts: int = 0
    hash_dict = dict()
    start = time.time()
    while True:
        attempts += 1
        suffix: str = ''.join(random.choices(string.ascii_letters + string.digits, k = 8))
        message: str = name + suffix
        hash_value = H(message)
        if hash_value in hash_dict:
            other_hash = hash_dict[hash_value]
            end = time.time()
            total = end - start
            print("================================")
            print(f"Hash: \t\t {hash_value}")
            print(f"Attempts: \t {attempts}")
            print(f"Value 1: \t {other_hash}")
            print(f"Value 2: \t {message}")
            print(f"Duration: \t {total}")
            print("================================")
            break
        else:
            hash_dict[hash_value] = message


if __name__ == '__main__':
    attack()
