import csv
#   from matplotlib import pyplot as plt

x, y = [], []
with open('sc.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    f = True
    for row in csvreader:
        if f:
            f = False
            continue
        x.append(float(row[0]))
        if (zn := (float(row[2]) + float(row[3])) / 2) > 2200:
            y.append(zn)
        else:
            y.append(0)


x = x[100:]
y = y[100:]

for i in range(1, 5899):
    y[i] = (y[i] + y[i - 1] + y[i + 1]) / 3

for i in range(0, 5800, 200):
    count = 0
    chunky = y[100+i:i+200]
    for cx in chunky:
        if cx > 100:
            count += 1
    if count > 10:
        print("1", end="")
    else:
        print("0", end="")

    # plt.plot(x[i+100:i+200], chunky)
    # plt.title('Plot of CSV')
    # plt.xlabel('X')
    # plt.ylabel('Y')
    # plt.show()

    # chunky = y[i + 50:i + 150]
    # peak = -1e9
    # for x in chunky:
    #     peak = max(peak, x)
    # if peak > (sum(y[i:i + 50]) + sum(y[i + 150:i + 200]) / 100):
    #     print(1, end="")
    # else:
    #     print(0, end="")

count = 0
chunky = y[5800:]
for cx in chunky:
    if cx > 100:
        count += 1
if count > 10:
    print("1", end="")
else:
    print("0", end="")