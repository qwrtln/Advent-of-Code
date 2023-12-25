import collections
import string

import numpy as np


puzzle = [line for line in open("inputs/22-sample.txt").read().strip().split("\n")]


def parse_lines(puzzle):
    coordinates = {}
    for i, line in enumerate(puzzle):
        start, end = line.split("~")
        # coordinates[string.ascii_uppercase[i]] = (tuple(int(i) for i in start.split(",")), tuple(int(i) for i in end.split(",")))
        coordinates[i] = (
            tuple(int(i) for i in start.split(",")),
            tuple(int(i) for i in end.split(",")),
        )
    return coordinates


def find_max(coordinates, which):
    i = ("x", "y", "z").index(which)
    return max(
        max(coordinates.values(), key=lambda c: (c[0][i], c[1][i])), key=lambda c: c[i]
    )[i]


def is_brick_floating(c, bricks):
    (x0, y0, z0), (x1, y1, z1) = c
    if z0 == 1 or z1 == 1:
        # this brick is on the ground
        return False
    if x0 == x1 and y0 == y1:
        # this is a vertical brick
        z = min(z0, z1)
        if bricks[x0][y0][z - 1] == 1:
            return False
        return True
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                if bricks[x][y][z - 1] == 1:
                    return False
    return True


def move_brick_down(k, coordinates, bricks):
    (x0, y0, z0), (x1, y1, z1) = coordinates[k]
    coordinates[k] = ((x0, y0, z0 - 1), (x1, y1, z1 - 1))
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                bricks[x][y][z] = 0
                bricks[x][y][z - 1] = 1


coordinates = parse_lines(puzzle)

max_x = find_max(coordinates, "x")
max_y = find_max(coordinates, "y")
max_z = find_max(coordinates, "z")

bricks = np.zeros((max_x + 1, max_y + 1, max_z + 1))

for c in coordinates.values():
    (x0, y0, z0), (x1, y1, z1) = c
    brick_size = 0
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                brick_size += 1
                bricks[x][y][z] = 1

bricks_moved = False
while not bricks_moved:
    moved = False
    for k, c in coordinates.items():
        if is_brick_floating(c, bricks):
            move_brick_down(k, coordinates, bricks)
            moved = True
    if not moved:
        bricks_moved = True


point_to_brick_map = {}
for k, c in coordinates.items():
    (x0, y0, z0), (x1, y1, z1) = c
    brick_size = 0
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                point_to_brick_map[(x, y, z)] = k


brick_supporting_map = collections.defaultdict(set)
for k, c in coordinates.items():
    (x0, y0, z0), (x1, y1, z1) = coordinates[k]
    brick_supporting_map[k]
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                below = (x, y, z - 1)
                if below in point_to_brick_map and point_to_brick_map[below] != k:
                    brick_supporting_map[k].add(point_to_brick_map[below])


sole_supporters = 0
for k in brick_supporting_map:
    only_supporter = False
    for v in brick_supporting_map.values():
        if k in v and len(v) == 1:
            only_supporter = True
    if only_supporter:
        sole_supporters += 1

result = len(coordinates) - sole_supporters
print("1:", result)
