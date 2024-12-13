# Benchmark: CPython (3.12.7)
#   Time (mean ± σ):     983.0 ms ±  25.5 ms    [User: 1511.0 ms, System: 14.6 ms]
#   Range (min … max):   947.6 ms … 1024.5 ms    10 runs
#
# Benchmark: pypy (3.10.14-7.3.17)
#   Time (mean ± σ):     14.889 s ±  0.259 s    [User: 15.332 s, System: 0.046 s]
#   Range (min … max):   14.444 s … 15.317 s    10 runs
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
    islands = []

    def flood_fill(i, j, island):
        try:
            if not mask[(i, j)] or visited[(i, j)]:
                return
        except IndexError:
            return
        visited[(i, j)] = 1
        island.append((i, j))
        for nei in get_neighbours(i, j):
            flood_fill(*nei, island)

    for x_c, y_c in zip(x, y):
        if mask[(x_c, y_c)] and not visited[(x_c, y_c)]:
            island = []
            flood_fill(x_c, y_c, island)
            islands.append(island)

    return islands


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
        neighbours = [(int(x + dx), int(y + dy)) for dx, dy in mask]
        in_island = [int(p in island) for p in neighbours]
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
    for x, y in island:
        dd = ((-1, 0), (1, 0), (0, -1), (0, 1))
        for dx, dy in dd:
            x_n = x + dx
            y_n = y + dy
            if (
                not (0 <= x_n < WIDTH)
                or not (0 <= y_n < HEIGHT)
                or GARDEN[(x_n, y_n)] != plant
            ):
                boundary.add((x, y))
                perimiter += 1
        # fmt: off
        UL, UC, UR = (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
        CL, _,  CR = (x - 1, y),      None,      (x + 1, y    )
        DL, DC, DR = (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)
        # fmt: on
        # .E.
        # EEE <- points for a special case
        # .E.
        if (
            0 <= x + 1 < WIDTH
            and 0 <= x - 1 < WIDTH
            and 0 <= y + 1 < HEIGHT
            and 0 <= y - 1 < HEIGHT
            and all(n in island for n in [UC, CR, DC, CL])
            and any(n not in island for n in [UL, UR, DR, DL])
        ):
            boundary.add((x, y))
    return perimiter, boundary


result_1 = 0
result_2 = 0
for plant in get_plants(GARDEN):
    x, y = np.where(GARDEN == plant)
    area = np.array([x, y]).T
    islands = find_islands(x, y, plant, GARDEN)
    for island in islands:
        area = np.array(island).size // 2
        perimiter, boundary_points = calculate_perimiter(island, plant)
        result_1 += area * perimiter
        corners = 0
        for p in boundary_points:
            c = count_point_corners(p, island)
            corners += count_point_corners(p, island)
        result_2 += area * corners


print("1:", result_1)
print("2:", result_2)
