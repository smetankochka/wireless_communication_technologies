import sys
from scipy.fft import rfft, rfftfreq


normalized_tone = sys.stdin.read().split()
res = []
for i in range(1, len(normalized_tone), 2):
    res.append(normalized_tone[i])
N = 8000

yf = list(abs(rfft(res)))
xf = list(rfftfreq(N, 1 / 8000))
t = sorted(yf, key=lambda x: -x)
f = []
s = []
for i in t:
    fl = True
    for j in f:
        if abs(j[0] - xf[yf.index(i)]) < 10:
            fl = False
    if fl:
        f.append((xf[yf.index(i)], i))
    if len(f) == 3:
        break

for i in sorted(f, key=lambda x: -x[1]):
    s.append(i[0])
print(*s)
# 1313.0 543.0 328.0