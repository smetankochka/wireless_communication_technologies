import sys

data = [x.split("\t") for x in list(map(str.strip, sys.stdin))[1:]]
channels = [0] * 28
for _, channel, percent in data:
    channels[int(channel)] += float(percent)
ans, minimal = -1, 1
for channel, percent in enumerate(channels):
    if minimal > percent:   # если рассматриваем только используемые, то ...and percent != 0
        minimal = percent
        ans = channel
print(ans)
