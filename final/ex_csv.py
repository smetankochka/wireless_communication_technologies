import csv
import numpy as np

x, y = [], []
with open('sample-1.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    f = True
    for row in csvreader:
        if f:
            f = False
            continue
        x.append(float(row[0]))
        y.append(((float(row[2]) + float(row[3])) - 4000) / 2)

dydx = np.gradient(y, x)
for i in range(0, 6000, 375):
    flag = False
    chunky = y[i:i+375]
    peak = -1e9
    for j in range(50):
        peak = max(peak, chunky[j])
    for j in range(375 - 50):
        if chunky[j] > 2 * peak:
            flag = True
            break
    if flag:
        print(1, end="")
    else:
        print(0, end="")