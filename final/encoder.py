def decoder(filein, fileout, filelog, block_size: int = 256):
    try:
        block_size = 256
        packets = {}
        number_list = []
        count = -1
        while True:
            count += 1
            s = filein.read(block_size)
            print(s)
            if not s:
                break
            number = s[0]
            print(number)
            if number not in number_list:
                number_list.append(number)
            s = s[1:].replace(b';', b'')
            packets[number] = s
        print(sorted(number_list))
        print(count)
        for i in sorted(list(number_list)):
            fileout.write(packets[i])

    except Exception as e:
        print(str(e))