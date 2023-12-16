import math


def to_degrees(x):
    return x * (180 / math.pi)


def to_radian(x):
    return x / (180 / math.pi)


def calc_azimut(x):
    if 0 <= x <= 90:
        return 90 - x
    elif 90 <= x <= 180:
        return 450 - x
    elif 180 <= x <= 270:
        return 450 - x
    else:
        return 450 - x


n, index, x, y = list(map(float, input().split()))
n, index = int(n), int(index)
cords = []
for i in range(n):
    xi, yi = list(map(float, input().split()))
    cords.append([xi - x, yi - y])

angles = []
for i, (xi, yi) in enumerate(cords):
    if xi == 0 and yi >= 0:
        angles.append([90.0, i])
    elif xi == 0 and yi < 0:
        angles.append([270.0, i])
    elif yi == 0 and xi >= 0:
        angles.append([0.0, i])
    elif yi == 0 and xi < 0:
        angles.append([180.0, i])
    elif xi > 0 and yi > 0:
        angle = to_degrees(math.atan(yi / xi))
        angles.append([angle, i])
    elif xi < 0 and yi > 0:
        angle = to_degrees(math.atan(yi / xi))
        angles.append([180 - abs(angle), i])
    elif xi > 0 and yi < 0:
        angle = to_degrees(math.atan(yi / xi))
        angles.append([360 - abs(angle), i])
    elif xi < 0 and yi < 0:
        angle = to_degrees(math.atan(yi / xi))
        angles.append([180 + angle, i])
# print(*angles)
azimuts = [calc_azimut(angles[i][0]) for i in range(n)]
# print(*azimuts)
angles.sort()
new_index = -1
for i in range(n):
    if angles[i][1] == index:
        new_index = i
# print(*angles)
# azimut = calc_azimut(angles[new_index][0])

# print(new_index)
if n == 1:
    print(to_radian(calc_azimut(angles[new_index][0])), 360.0)
elif n == 2:
    print(to_radian(calc_azimut((angles[1 - new_index][0] + 180) % 360.0)), 360.0)
else:
    if new_index != n - 1:
        mx_ugol = abs(angles[(new_index - 1) % n][0] - angles[(new_index + 1) % n][0])
        azimut = (angles[(new_index - 1) % n][0] + angles[(new_index + 1) % n][0]) / 2
        azimut = calc_azimut(azimut)
    else:
        mx_ugol = angles[0][0] + 360 - angles[n - 2][0]
        azimut = (angles[n - 2][0] + mx_ugol / 2) % 360.0
        azimut = calc_azimut(azimut)
    print(to_radian(azimut), mx_ugol)
