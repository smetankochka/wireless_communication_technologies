with open("input_second.txt", "r") as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        with open(str(i + 1) + ".txt", "w") as out:
            for _ in range(3):
                for j, bit in enumerate([int(x) for x in line.strip()]):
                    if not bit:
                        out.write("0\n" * 66)
                        continue
                    out.write("0\n" * 23)
                    out.write("4095\n" * 20)
                    out.write("0\n" * 23)
            out.write("0\n" * 60)