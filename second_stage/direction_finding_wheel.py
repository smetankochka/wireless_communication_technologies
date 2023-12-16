# import matplotlib.pyplot as plt
import sys


def find_intersection_line_circle(x0, y0, r0, a, b, c):
    d = (2 * a * c - 2 * b ** 2 * x0 + 2 * a * b * y0) ** 2 - 4 * (a ** 2 + b ** 2) * \
        (b ** 2 * x0 ** 2 + b ** 2 * y0 ** 2 + c ** 2 + 2 * y0 * b * c - r0 ** 2 * b ** 2)
    if d >= 0:
        x1 = (-(2 * a * c - 2 * b ** 2 * x0 + 2 * a * b * y0) + d ** (1 / 2)) / (2 * (a ** 2 + b ** 2))
        x2 = (-(2 * a * c - 2 * b ** 2 * x0 + 2 * a * b * y0) - d ** (1 / 2)) / (2 * (a ** 2 + b ** 2))
        y1, y2 = (-c - a * x1) / b, (-c - a * x2) / b
        return [[x1, y1], [x2, y2]]
    else:
        return None


def find_intersection_circle_circle(x1, y1, r1, x2, y2, r2):
    x2, y2 = x2 - x1, y2 - y1
    res = find_intersection_line_circle(0, 0, r1, 2 * x2, 2 * y2, -(x2 ** 2 + y2 ** 2 + r1 ** 2 - r2 ** 2))
    if res is not None:
        x11, y11, x22, y22 = res[0][0] + x1, res[0][1] + y1, res[1][0] + x1, res[1][1] + y1
        return [[x11, y11], [x22, y22]]
    else:
        return None


def find_intersection_line_line(a1, b1, c1, a2, b2, c2):
    if b1 == 0:
        return [-c1 / a1, (-c2 - a2 * (-c1 / a1)) / b2]
    x = (b2 * c1 - c2 * b1) / (a2 * b1 - b2 * a1)
    y = -(c1 + a1 * x) / b1
    return [x, y]


def find_line(x1, y1, x2, y2):
    a = 1 if y1 != y2 else 0
    b = (x2 - x1) / (y1 - y2) if y2 != y1 else 1
    c = -(x1 + b * y1)
    return [a, b, c]


def find_perpendicular(a, b, c, x, y):
    return [-b, a, b * x - a * y]


def find_center(x1, y1, x2, y2, x3, y3):
    mx1, my1, mx2, my2 = (x1 + x2) / 2, (y1 + y2) / 2, (x2 + x3) / 2, (y2 + y3) / 2
    a1, b1, c1 = find_line(x1, y1, x2, y2)
    a2, b2, c2 = find_line(x2, y2, x3, y3)
    a1p, b1p, c1p = find_perpendicular(a1, b1, c1, mx1, my1)
    a2p, b2p, c2p = find_perpendicular(a2, b2, c2, mx2, my2)
    xc, yc = find_intersection_line_line(a1p, b1p, c1p, a2p, b2p, c2p)
    return [xc, yc]


def find_radius(xc, yc, x1, y1):
    return ((xc - x1) ** 2 + (yc - y1) ** 2) ** (1 / 2)


lines = sys.stdin.readlines()
x1, y1 = list(map(float, lines[0].split()))
x2, y2 = list(map(float, lines[1].split()))
x3, y3 = list(map(float, lines[2].split()))

pings = []
v = 343
for i in range(len(lines) - 3):
    s = lines[3 + i]
    pings.append([int(s.split()[0]), (float(s.split()[1]) - 10) / 2,
                  (float(s.split()[2]) - 10) / 2, (float(s.split()[3]) - 10) / 2])

dists = [[ping[1] / 1000 * v, ping[2] / 1000 * v, ping[3] / 1000 * v] for ping in pings]
# print(*dists)
# print(find_intersection_line_circle(0, 0, 1, 1, -1, 0))
# print(find_intersection_circle_circle(1, 2, 1, 1, -1, 2))
n = len(dists)

# print(find_center(1, 0, -1, 0, 0.707, 0.707))
puncts = []
for i in range(len(dists)):
    d1, d2, d3 = dists[i][0], dists[i][1], dists[i][2]
    res1 = find_intersection_circle_circle(x1, y1, d1, x2, y2, d2)
    res2 = find_intersection_circle_circle(x1, y1, d1, x3, y3, d3)
    res3 = find_intersection_circle_circle(x2, y2, d2, x3, y3, d3)
    point1, point2 = [round(res1[0][0], 6), round(res1[0][1], 6)], [round(res1[1][0], 6), round(res1[1][1], 6)]
    point3, point4 = [round(res2[0][0], 6), round(res2[0][1], 6)], [round(res2[1][0], 6), round(res2[1][1], 6)]
    point5, point6 = [round(res3[0][0], 6), round(res3[0][1], 6)], [round(res3[1][0], 6), round(res3[1][1], 6)]

    points1, points2, points3 = [point1, point2], [point3, point4], [point5, point6]
    points = [point1, point2, point3, point4, point5, point6]

    for point in points:
        if point in points1 and point in points2 and point in points3:
            puncts.append(point)
            break

# xc1, yc1 = find_center(puncts[0][0], puncts[0][1], puncts[1][0], puncts[1][1], puncts[2][0], puncts[2][1])
# xc2, yc2 = find_center(puncts[3][0], puncts[3][1], puncts[4][0], puncts[4][1], puncts[5][0], puncts[5][1])
xc, yc = find_center(puncts[0][0], puncts[0][1], puncts[1][0], puncts[1][1], puncts[2][0], puncts[2][1])
radius = find_radius(xc, yc, puncts[0][0], puncts[0][1])
x = [puncts[i][0] for i in range(len(puncts))]
y = [puncts[i][1] for i in range(len(puncts))]

print(xc, yc, radius)
# print(find_perpendicular(1, -1, 0, 1, 1))
# plt.scatter(x, y)
# plt.show()
# print(find_perpendicular(1, -1, 0, 1, 1))
