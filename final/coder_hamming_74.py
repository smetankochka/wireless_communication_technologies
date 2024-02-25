import itertools

def hamming_code(data):
    hamming_table = [
        [0, 0, 0, 0, 0, 0, 0],  # 000
        [1, 1, 0, 1, 0, 1, 0],  # 001
        [1, 0, 1, 1, 0, 0, 1],  # 010
        [0, 1, 1, 1, 1, 0, 0],  # 011
        [1, 1, 1, 0, 0, 0, 1],  # 100
        [0, 0, 1, 0, 1, 1, 1],  # 101
        [0, 1, 0, 0, 1, 1, 1],  # 110
        [1, 0, 0, 0, 0, 1, 1]   # 111
    ]
    hamming_data = []
    for byte in data:
        bits = [int(b) for b in bin(byte)[2:].zfill(8)]
        chunked_bits = [bits[i:i+4] for i in range(0, len(bits), 4)]
        for chunk in chunked_bits:
            hamming_chunk = list(itertools.chain(*[hamming_table[b] for b in chunk]))
            hamming_data.extend(hamming_chunk)
    return bytes(hamming_data)


with open("in.txt", "rb") as input_file:
    data = input_file.read()
    encoded_data = hamming_code(data)

with open("out.txt", "wb") as output_file:
    output_file.write(encoded_data)