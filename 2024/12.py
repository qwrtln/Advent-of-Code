# Benchmark: CPython (3.12.7)
#  Time (mean ± σ):     634.5 ms ±  24.7 ms    [User: 1147.0 ms, System: 13.7 ms]
#  Range (min … max):   602.1 ms … 684.2 ms    10 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#  Time (mean ± σ):      8.257 s ±  0.235 s    [User: 8.701 s, System: 0.037 s]
#  Range (min … max):    7.912 s …  8.736 s    10 runs
#
import numpy as np

GARDEN = np.array(
    [list(line) for line in open("inputs/12.txt").read().strip().split("\n")]
)

WIDTH, HEIGHT = GARDEN.shape


def get_plants(garden):
    plants = set()
    for row in garden:
        plants.update(row)
    return plants


def get_neighbours(x, y):
    dd = ((-1, 0), (1, 0), (0, -1), (0, 1))
    for dx, dy in dd:
        x_n = x + dx
        y_n = y + dy
        if 0 <= x_n < WIDTH and 0 <= y_n < HEIGHT:
            yield x_n, y_n


def find_islands(x, y, plant, garden):
    mask = (garden == plant).astype(int)
    visited = np.zeros_like(mask)

    def flood_fill(i, j, island):
        if not mask[(i, j)] or visited[(i, j)]:
            return
        visited[(i, j)] = 1
        island.append((i, j))
        for nei in get_neighbours(i, j):
            flood_fill(*nei, island)

    for x_c, y_c in zip(x, y):
        if mask[(x_c, y_c)] and not visited[(x_c, y_c)]:
            island = []
            flood_fill(x_c, y_c, island)
            yield island


def count_point_corners(point, island):
    x, y = point
    # fmt: off
    matrices = [
            [(-1, -1), ( 0, -1),  # 12.
             (-1,  0),         ], # 3x.
            #-----------------    # ...

            [( 0, -1), ( 1, -1),  # .12
                       ( 1,  0)], # .x3
            #-----------------    # ...

            [          ( 1,  0),  # ...
             ( 0,  1), ( 1,  1)], # .x1
            #-----------------    # .23

            [(-1,  0),            # ...
             (-1,  1), ( 0,  1)], # 1x.
            #-----------------    # 23.
    ]
    convex = [[0, 1, 1],
              [1, 0, 1],
              [1, 1, 0],
              [1, 0, 1],
              ]
    concave = [[1, 0, 0],
               [0, 1, 0],
               [0, 0, 1],
               [0, 1, 0],
              ]
    # fmt: on
    corners = 0
    for index, mask in enumerate(matrices):
        in_island = [int((int(x + dx), int(y + dy)) in island) for dx, dy in mask]
        if sum(in_island) == 0:
            corners += 1
        if in_island == concave[index]:
            corners += 1
        if in_island == convex[index]:
            corners += 1
    return corners


def calculate_perimiter(island, plant):
    perimiter = 0
    boundary = set()
    nei_ortho = ((-1, 0), (1, 0), (0, -1), (0, 1))
    nei_diag = ((-1, -1), (-1, 1), (1, -1), (1, 1))
    for x, y in island:
        if any((x + dx, y + dy) not in island for dx, dy in [*nei_ortho, *nei_diag]):
            boundary.add((x, y))
        for dx, dy in nei_ortho:
            x_n = x + dx
            y_n = y + dy
            if (
                not (0 <= x_n < WIDTH)
                or not (0 <= y_n < HEIGHT)
                or GARDEN[(x_n, y_n)] != plant
            ):
                perimiter += 1
    return perimiter, boundary


result_1 = 0
result_2 = 0
for plant in get_plants(GARDEN):
    x, y = np.where(GARDEN == plant)
    area = np.array([x, y]).T
    for island in find_islands(x, y, plant, GARDEN):
        area = np.array(island).size // 2
        perimiter, boundary_points = calculate_perimiter(island, plant)
        result_1 += area * perimiter
        corners = sum(count_point_corners(p, island) for p in boundary_points)
        result_2 += area * corners


print("1:", result_1)
print("2:", result_2)
