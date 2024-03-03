def encoder(filein, fileout):
    blocksize = 1023
    num = 1
    code = True
    pakets = []
    while code:
        s = filein.read(blocksize)
        if len(s) != 1023:
            code = False

        s += bytes([0] * (1023 - len(s)))

        if num > 255:
            raise Exception("Переполнение")
        number = bytes([num])
        num += 1
        paket = number + s
        pakets.append(paket)

    offset = len(pakets) // 7


    for i in pakets:
        fileout.write(i)
    for i in range(1, 9):
        for j in pakets[i * offset:]:
            fileout.write(j)
        for j in pakets[:i * offset]:
            fileout.write(j)


if __name__ == "__main__":
    filein = open("test.txt", "rb")
    fileout = open("out.txt", "wb")
    encoder(filein, fileout)
