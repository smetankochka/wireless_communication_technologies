def hamming(data: bytes):
    CONTROL_BITS = [0, 1, 3, 7, 15, 31]

    result = ''

    for block in range(-len(data) // 64 * -1):
        start = block * 64
        end = start + 64

        chunk: str = data[start:end]
        control_data = [0 for i in range(6)]
        data_chunk = ''
        errors = []

        for i in range(63):
            if i in CONTROL_BITS:
                continue

            for j in range(6):
                if (i + 1) & (1 << j):
                    control_data[j] ^= int(chunk[i])

        for i, val in enumerate(CONTROL_BITS):
            if chunk[val] != str(control_data[i]):
                errors.append(val + 1)

        if errors:
            bit = sum(errors) - 1
            chunk = list(chunk)
            chunk[bit] = str(1 - int(chunk[bit]))
            chunk = ''.join(chunk)

        for i in range(63):
            if i in CONTROL_BITS:
                continue
            result += chunk[i]
    return result


def decoder(filein, fileout, filelog):
    blocksize = 1024
    block_num = 0
    packets = {}
    maxN = 0

    while True:
        s = filein.read(blocksize)
        if not s:
            break

        s1 = f"{bin(int.from_bytes(s, 'big'))[2:]:>08192}"
        s1 = hamming(s1)
        print(len(s1))
        s = int(s1, 2).to_bytes(913, 'big')

        n = int.from_bytes(s[1:3], 'big')
        maxN = max(maxN, n)

        s = s[3:].replace(b';', b'')

        packets[n] = s

    for i in range(maxN + 1):
        if i in packets:
            fileout.write(packets[i])
        else:
            fileout.write(packets[0])


if __name__ == '__main__':
    decoder(open('encoded.dat', 'rb'), open('decoded.dat', 'wb'), '')