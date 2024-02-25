def hamming(data: bytes):
    CONTROL_BITS = [0, 1, 3, 7, 15, 31]

    result = ''

    for block in range(-len(data) // 57 * -1):
        start = block * 57
        end = start + 57

        chunk: bytes = data[start:end]
        control_data = [0 for i in range(6)]

        for i in CONTROL_BITS:
            chunk = chunk[:i] + '0' + chunk[i:]

        for i in range(63):
            if i in CONTROL_BITS:
                continue

            for j in range(6):
                if (i + 1) & (1 << j):
                    control_data[j] ^= int(chunk[i])

        for i, val in enumerate(CONTROL_BITS):
            chunk = f'{chunk[:val]}{control_data[i]}{chunk[val + 1:]}'
        result += chunk + '0'
    return result


def encoder(filein, fileout):
    blocksize = 910
    block_num = 0
    packets = []
    copies = 7

    while True:
        s = filein.read(blocksize)
        if not s:
            break

        s = block_num.to_bytes(2, 'big') + s
        block_num += 1
        s += b';' * (912 - len(s))

        s1 = f'{bin(int.from_bytes(s, "big"))[2:]:>07296}'
        s1 = hamming(s1)
        print(len(s1))
        s = int(s1, 2).to_bytes(1024, 'big')

        packets.append(s)

    for i in range(copies):
        # print(i)
        for pack in packets:
            fileout.write(pack)
        # map(fileout.write, packets)


if __name__ == '__main__':
    encoder(open('test.dat', 'rb'), open('encoded.dat', 'wb'))
