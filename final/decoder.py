def decoder(filein, fileout, filelog):
    blocksize = 1024
    data = {}
    max_num = 0
    code = True
    while code:
        s = filein.read(blocksize)
        if not s:
            break
        num = int(s[0])
        zero = bytes([0])
        data[num] = s[1:].replace(zero, b"")
        max_num = max(num, max_num)
    for i in range(1, max_num+1):
        try:
            fileout.write(data[i])
        except KeyError:
            if i != max_num+1:
                fileout.write(b"0"*1023)
            else:
                pass
