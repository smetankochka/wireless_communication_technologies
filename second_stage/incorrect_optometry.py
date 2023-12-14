import sys
import math

data = [x.split() for x in list(map(str.strip, sys.stdin))]
time = [0] * len(data)
length = [0] * len(data)
mintime = 1e18
maxtime = -1e18
infall = 0
for i, cor in enumerate(data):
    inform = int(cor[1][8:12], 16) * 8 + 64 + 160
    infall += inform
    timenow = int(cor[0]) / 1000
    if timenow < mintime:
        mintime = timenow
    if timenow > maxtime:
        maxtime = timenow
print(math.floor(infall / (maxtime - mintime)))