import itertools

import numpy as np
from matplotlib.path import Path

puzzle = [line for line in open("inputs/09.txt").read().strip().split("\n")]

points = []
for line in puzzle:
    x, y = line.split(",")
    points.append((int(x), int(y)))


def find_max_red(points):
    max = 0
    for p1, p2 in itertools.combinations(points, 2):
        x1, y1 = p1
        x2, y2 = p2
        area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        if area > max:
            max = area
    return max


print("1:", find_max_red(points))


x_coords = [p[0] for p in points]
y_coords = [p[1] for p in points]
x_size = max(x_coords)
y_size = max(y_coords)

polygon = Path(points)

max_dist = 0
max_index = 0
for i, x in enumerate(x_coords[1:]):
    dist = x - x_coords[i - 1]
    if dist > max_dist:
        max_dist = dist
        max_index = i + 1

p_north = points[max_index]
p_south = points[max_index + 1]

x_o = [p_north[0], p_south[0]]
y_o = [p_north[1], p_south[1]]


def is_rectangle_in(point, y_limit, x_limit, polygon, direction):
    x, y = point
    vertical_line = np.array([[x, i] for i in range(y, y_limit, direction)])
    horizontal_line = np.array([[i, y] for i in range(x, x_limit)])
    return (vertical_line.size == 0 or horizontal_line.size == 0) or (
        polygon.contains_points(horizontal_line).all()
        and polygon.contains_points(vertical_line).all()
    )


max_candidate_area_n = 0
max_candidate_n = (0, 0)
x_m, y_m = p_north
for i in range(max_index - 1, 0, -1):
    candidate = points[i]
    if candidate[1] > y_size * 0.75:
        break
    if is_rectangle_in(candidate, p_north[1], p_north[0], polygon, -1):
        x_c, y_c = candidate
        area = (abs(x_m - x_c) + 1) * (abs(y_m - y_c) + 1)
        if area > max_candidate_area_n:
            max_candidate_n = candidate
            max_candidate_area_n = area

max_candidate_area_s = 0
max_candidate_s = (0, 0)
x_m, y_m = p_south
min_s = min(y_coords)

for i in range(max_index + 1, len(points)):
    candidate = points[i]
    if candidate[1] < (y_m - min_s) * 0.5:
        break
    if is_rectangle_in(candidate, p_south[1], p_south[0], polygon, 1):
        x_c, y_c = candidate
        area = (abs(x_m - x_c) + 1) * (abs(y_m - y_c) + 1)
        if area > max_candidate_area_s:
            max_candidate_s = candidate
            max_candidate_area_s = area


print("2:", max(max_candidate_area_n, max_candidate_area_s))
