def s_box(s = 170):
    array = []
    for i in range(256):
        array.append(s)
        s = (37 * s + 9) % 256
    return array


def left_rot(val, shift, width = 128):
    for x in range(shift % width):
        msb = (val >> (width - 1)) & 1  # höchstes Bit extrahieren
        val = ((val << 1) & ((1 << width) - 1)) | msb  # links shiften & MSB rechts anhängen
    return val


def K(key = 0xdeadbeef000000000000000badc0ffee):
    array = []
    k_prev = key
    for i in range(32):
        rot = left_rot(k_prev, 7 * i, 128)
        k = rot ^ 0xabcdef
        khex = format(k, '032x')
        array.append(khex)
        k_prev = k
    return array


def text_to_hex(text: str):
    hex_str = text.encode("utf-8").hex()
    return hex_str


def F(block, k):
    sbox = s_box()
    k_bin = bin(k).removeprefix("0b").zfill(128)
    lsb = k_bin[64:]
    msb = k_bin[:64]

    #print(k, len(k))
    #print(lsb, len(lsb))
    #print(msb, len(msb))

    lsb_int = int(''.join(map(str, lsb)), 2)
    msb_bit = int(''.join(map(str, msb)), 2)

    xor = (block ^ msb_bit) & 0xFFFFFFFFFFFFFFFF

    xor_str = f"{xor:016x}"
    #print(xor_str, type(xor_str))
    merge_array = []

    for i in range(0, 16, 2):
        #print(xor_str)
        byte = xor_str[i:i + 2]
        #print(byte)
        byte_int = int(byte, 16)
        #print(byte_int)
        s = sbox[byte_int]
        #print(s)
        merge_array.append(s)
    # print(merge_array)
    merge_array
    merged: bytes = b""
    for merged_byte in merge_array:
        byte = merged_byte.to_bytes()
        merged += byte
    hex_text = int.from_bytes(merged, "big")
    # print(hex(int(merged, 16)))

    # print(hex(merged_sbox))
    # print(hex(lsb))

    xor_final = hex_text ^ lsb_int

    return xor_final


def E(text):
    hextext = text_to_hex(text)
    6
    k = K()
    for i in range(32):
        #print(hextext)
        l = hextext[:16]
        r = hextext[16:]
        # print(r, l)
        l, r = r, (l ^ F(r, k[i]))
    r, l = l, r

    return l + r


def test_functions():
    k = K()
    #print(k[0])
    assert "deadbeef000000000000000bad6b3201" == k[0]
    assert "56df778000000000000005d6b532cd00" == k[1]
    assert "dde00000000000000175ad4cb3ebd858" == k[2]
    assert "770feb4b3180dc3bc09870bd38e2cb5f" == k[31]
    print("Schlüssel erfolgreich erstellt...")

    sbox = s_box()
    #print(sbox)
    assert 170 == sbox[0]
    assert 155 == sbox[1]
    assert 112 == sbox[2]
    assert 33 == sbox[123]
    assert 205 == sbox[255]
    print("S-Box erfolgreich erstellt...")

    print("\n" + "*" * 35, "\n")
    print("TEST ABGESCHLOSSEN")


if __name__ == '__main__':
    text = "test"
    # encrypted_text = E(text)
    x = F(0xb0aa7cca50e95fb1, 0xdde00000000000000175ad4cb3ebd858)
    k = K()
    print(k[1])
    print("Done", hex(x))
    # test_functions()