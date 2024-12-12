import enum

import numpy as np

GARDEN = np.array(
    [list(line) for line in open("inputs/12.txt").read().strip().split("\n")]
)

WIDTH, HEIGHT = GARDEN.shape


class Direction(enum.Enum):
    VERTICAL = enum.auto()
    HORIZONTAL = enum.auto()
    DIAGONAL = enum.auto()


def get_plants(garden):
    plants = set()
    for row in garden:
        plants.update(row)
    return plants


for line in GARDEN:
    print("".join(line))
print("---------------")


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


def calculate_perimiter(island, plant):
    perimiter = 0
    boundary = []
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
                if (x, y) not in boundary:
                    boundary.append((x, y))
                perimiter += 1
    return perimiter, boundary


DIRECTION_MAPPING = {
    (0, 1): Direction.VERTICAL,
    (0, -1): Direction.VERTICAL,
    (1, 0): Direction.HORIZONTAL,
    (-1, 0): Direction.HORIZONTAL,
}


def calculate_sides(boundary_points):
    lines = []
    current_line = [boundary_points[0]]

    def get_direction(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]


def plot_garden(point, plant):
    plot = ""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x, y) == point:
                plot += "."
            elif GARDEN[y][x] == plant:
                plot += GARDEN[y][x]
            else:
                plot += " "
        plot += "\n"
    print(plot)


result_1 = 0
for plant in get_plants(GARDEN):
    x, y = np.where(GARDEN == plant)
    area = np.array([x, y]).T
    islands = find_islands(x, y, plant, GARDEN)
    for island in islands:
        area = np.array(island).size // 2
        perimiter, boundary = calculate_perimiter(island, plant)
        result_1 += area * perimiter
        # plant_to_plot = "B"
        # if plant == plant_to_plot:
        #     for point in boundary:
        #         plot_garden(point, plant_to_plot)
        #         input("-------------------")

print("1:", result_1)
