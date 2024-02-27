import sys

data = [x.split(",") for x in [line.strip() for line in sys.stdin]][-6000:]

x, y = [], []
for row in data:
    x.append(float(row[0]))
    y.append((float(row[2]) + float(row[3])) / 2)

for i in range(0, 6000, 200):
    chunky = y[i+50:i+150]
    peak = -1e9
    for x in chunky:
        peak = max(peak, x)
    if peak > 1.2 * (sum(y[i:i+50]) + sum(y[i+150:i+200]) / 100):
        print(1, end="")
    else:
        print(0, end="")