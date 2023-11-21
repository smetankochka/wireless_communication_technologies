import sys
import math

data = [x.split() for x in list(map(str.strip, sys.stdin))]
sums = 0
for i, cor in enumerate(data):
    inf = len(bin(int(cor[1], 16))[2:])
    sums += inf
    data[i] = tuple([int(cor[0]) / 1000, inf])
data = sorted(data)
start, finish = data[0][0], data[-1][0]
print(start, finish)
t = finish - start
print(math.floor(sums / t))
