with open("input_second.txt", "r") as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        with open(str(i + 1) + ".txt", "w") as out:
            for j, bit in enumerate([int(x) for x in line.strip()]):
                if not bit:
                    out.write("0\n" * 200)
                    continue
                out.write("0\n" * 50)
                out.write("3750\n" * 33)
                out.write("0\n" * 33)
                out.write("3750\n" * 34)
                out.write("0\n" * 50)