import csv

x, y = [], []
now_list = []
with open('ta1.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for i in csvreader:
        print(i)
print(csvreader)
 #   f = True
 #   for row in csvreader:
 #       if f:
 #           f = False
 #           continue
 #       x.append(float(row[0]))
 #       if (zn := float(row[2])) > 2750:
 #           y.append(zn)
 #       else:
 #           y.append(0)

#
#for i in range(0, 6000, 375):
#    chunkx = x[i:i + 375]
#    chunky = y[i:i + 375]
#    toplet = 2750
#
    # plt.plot(chunkx, chunky)
    # plt.title('Plot of CSV')
    # plt.xlabel('X')
    # plt.ylabel('Y')
    # plt.show()

#    flag = False
#    for j in range(100):
#        if chunky[j] > toplet:
#            flag = True
#            break
#    if flag:
#        print(1, end="")
#    else:
#        print(0, end="")
#