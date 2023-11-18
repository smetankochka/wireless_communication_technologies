import sys

data = [x.split() for x in list(map(str.strip, sys.stdin))]
for i, cor in enumerate(data):
    data[i] = [int(cor[0]) / 1000, int(cor[1], 16)]
