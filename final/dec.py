
def hamming_7_4_decode(data):
    bits = [int(bit) for byte in data for bit in f'{byte:08b}']
    decoded_bits = [0, 0, 0, 0]
    decoded_bits[0] = bits[2]
    decoded_bits[1] = bits[4]
    decoded_bits[2] = bits[5]
    decoded_bits[3] = bits[6]
    p1 = bits[0] ^ bits[2] ^ bits[4] ^ bits[6]
    p2 = bits[1] ^ bits[2] ^ bits[5] ^ bits[6]
    p3 = bits[3] ^ bits[4] ^ bits[5] ^ bits[6]
    error_bit = p1 + p2 * 2 + p3 * 4 - 1
    if error_bit >= 0:
        bits[error_bit] = 1 - bits[error_bit]
    decoded_byte = bytes([int(''.join(map(str, decoded_bits)), 2)])
    return decoded_byte


def decoder(filein, fileout):
    blocksize = 9
    s = filein.read(blocksize)
    if not s:
        return
    while True:
        fileout.write(hamming_7_4_decode(s))
        s = filein.read(blocksize)
        if not s:
            break


f1 = open("out.txt", mode="rb")
f2 = open("in.txt", mode="wb")
decoder(f1, f2)
f1.close()
f2.close()