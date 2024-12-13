# Sadly, pt2 does not work
import numpy as np

GARDEN = np.array(
    [list(line) for line in open("inputs/12-test2.txt").read().strip().split("\n")]
)

WIDTH, HEIGHT = GARDEN.shape


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


def count_point_corners(point, island, plant=None):
    x, y = point
    # fmt: off
    UL, UC, UR = (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
    CL, _,  CR = (x - 1, y    ), None,       (x + 1, y    )
    DL, DC, DR = (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)
    # fmt: on
    up = [UL, UC, UR]
    down = [DL, DC, DR]
    left = [UL, CL, DL]
    right = [UR, CR, DR]
    diagonal = [UL, UR, DR, DL]
    orthogonal = [UC, CR, DC, CL]
    all_neighbours = [*orthogonal, *diagonal]
    sum_of_neighbours = sum(n in island for n in all_neighbours)
    if sum_of_neighbours == 0:
        return 4
    if sum_of_neighbours == 1:
        return 2
    if sum_of_neighbours == 2:
        if all(n in island for n in [UC, DC]) or (all(n in island for n in [CL, CR])):
            # e.g.
            #
            # ...
            # EEE
            # ...
            return 0
        if (
            all(n in island for n in up)
            or (all(n in island for n in down))
            or all(n in island for n in left)
            or (all(n in island for n in right))
        ):
            # e.g.
            #
            # .EE
            # .E.
            # ...
            return 2
        # e.g.
        #
        # .E.
        # .E.
        # E..
        return 2
    if sum_of_neighbours == 3:
        if (
            all(n in island for n in up)
            or (all(n in island for n in down))
            or (all(n in island for n in left))
            or (all(n in island for n in right))
        ):
            # ...
            # .E.
            # EEE
            return 2
        elif sum(n in island for n in diagonal) == 2:
            # E.E
            # .EE
            # ...
            return 2
        elif sum(n in island for n in diagonal) == 1 and (
            (sum(n in island for n in up) == 0 and sum(n in island for n in right) == 0)
            or (
                sum(n in island for n in right) == 0
                and sum(n in island for n in down) == 0
            )
            or (
                sum(n in island for n in down) == 0
                and sum(n in island for n in left) == 0
            )
            or (
                sum(n in island for n in left) == 0
                and sum(n in island for n in up) == 0
            )
        ):
            # ...
            # .EE
            # .EE
            return 1
        elif sum(n in island for n in diagonal) == 1 and (
            sum(n in island for n in (UC, DC)) == 2
            or sum(n in island for n in (CL, CR)) == 2
        ):
            # .E.
            # .E.
            # .EE
            return 0
        return 2
        # input("Always 2?")
    if sum_of_neighbours == 4:
        if all(n in island for n in orthogonal):
            # .E.
            # EEE
            # .E.
            return 4
        elif sum(n in island for n in diagonal) == 2 and (
            (all(n in island for n in up) and DC in island)
            or (all(n in island for n in down) and UC in island)
            or (all(n in island for n in left) and CR in island)
            or (all(n in island for n in right) and CL in island)
        ):
            # E..
            # EEE
            # E..
            return 0
        elif all(n in island for n in [UC, UL, UR, DR]) or (
            all(n in island for n in [UC, UR, CR, DL])
            or all(n in island for n in [CR, DR, DC, UL])
            or all(n in island for n in [DC, DL, CL, UR])
        ):
            # EE.
            # EE.
            # ..E
            return 1
        elif sum(n in island for n in diagonal) == 2 and (
            sum(n in island for n in (CL, CR)) == 2
            or sum(n in island for n in (UC, DC)) == 2
        ):
            # .EE
            # .E.
            # .EE
            return 0
        elif sum(n in island for n in diagonal) == 1 and (
            (sum(n in island for n in up) == 1 and sum(n in island for n in down) == 1)
            or (
                sum(n in island for n in right) == 1
                and sum(n in island for n in left) == 1
            )
        ):
            # ..E
            # EEE
            # .E.
            return 2
        elif sum(n in island for n in diagonal) == 2 and (
            (sum(n in island for n in left) == 2 and sum(n in island for n in up) == 2)
            or (
                sum(n in island for n in up) == 2
                and sum(n in island for n in right) == 2
            )
            or (
                sum(n in island for n in right) == 2
                and sum(n in island for n in down) == 2
            )
            or (
                sum(n in island for n in down) == 2
                and sum(n in island for n in left) == 2
            )
        ):
            # .EE
            # EE.
            # E..
            return 2
        else:
            # .EE
            # EE.
            # EE.
            return 1
        # elif all(n in island for n in down):
        # EEE
        # EEE
        # .E.
        # return 2
    if sum_of_neighbours == 5:
        if (
            (all(n in island for n in up) and CL in island and CR in island)
            or (all(n in island for n in down) and CL in island and CR in island)
            or (all(n in island for n in left) and UC in island and DC in island)
            or (all(n in island for n in right) and UC in island and DC in island)
        ):
            # EE.
            # EE.
            # EE.
            return 0
        elif (
            (
                all(n in island for n in up)
                and CL not in island
                and CR not in island
                and DC in island
            )
            or (
                all(n in island for n in down)
                and CL not in island
                and CR not in island
                and UC in island
            )
            or (
                all(n in island for n in left)
                and UC not in island
                and DC not in island
                and CR in island
            )
            or (
                all(n in island for n in right)
                and UC not in island
                and DC not in island
                and CL in island
            )
        ):
            # EEE
            # .E.
            # .EE
            return 0
        elif all(n in island for n in diagonal) and (
            all(n in island for n in up)
            or all(n in island for n in down)
            or all(n in island for n in left)
            or all(n in island for n in right)
        ):
            # EEE
            # .E.
            # E.E
            return 2
        else:
            # E.E
            # .EE
            # .EE
            return 1
    if sum_of_neighbours == 6:
        if sum(n in island for n in diagonal) == 4:
            # E.E
            # EEE
            # E.E
            return 0
        elif sum(n in island for n in orthogonal) == 4:
            # .E.
            # EEE
            # EEE
            return 2
        elif sum(n in island for n in diagonal) == 3 and (
            (all(n in island for n in up) and all(n in island for n in right))
            or (all(n in island for n in right) and all(n in island for n in down))
            or (all(n in island for n in down) and all(n in island for n in left))
            or (all(n in island for n in left) and all(n in island for n in up))
        ):
            # EE.
            # EE.
            # EEE
            return 0
        elif sum(n in island for n in diagonal) == 3 and (
            (all(n in island for n in right) and sum(n in island for n in left) == 2)
            or (all(n in island for n in left) and sum(n in island for n in right) == 2)
            or (all(n in island for n in up) and sum(n in island for n in down) == 2)
            or (all(n in island for n in down) and sum(n in island for n in up) == 2)
        ):
            # .EE
            # EEE
            # E.E
            return 1
        # else:
        #     # everything else
        #     #
        #     # E..
        #     # EEE
        #     # EEE
        #     return 0
        input("Unknown")
    if sum_of_neighbours == 7:
        non_neighbour = [n for n in all_neighbours if n not in island][0]
        if non_neighbour in orthogonal:
            # E.E
            # EEE <- rotated four times
            # EEE
            return 2
        else:
            # EE.
            # EEE <- rotated four times
            # EEE
            return 1

    print("Well well")
    # plot_garden(all_neighbours, plant)
    return 0


def calculate_perimiter(island, plant):
    perimiter = 0
    boundary = set()
    for x, y in island:
        # For a special case
        UL, UC, UR = (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
        CL, _, CR = (x - 1, y), None, (x + 1, y)
        DL, DC, DR = (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)
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


def plot_garden(point, plant):
    plot = ""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (y, x) == point:
                plot += "."
            elif GARDEN[y][x] == plant:
                plot += GARDEN[y][x]
            else:
                plot += " "
        plot += "\n"
    print(plot)


result_1 = 0
result_2 = 0
message = []
for plant in get_plants(GARDEN):
    x, y = np.where(GARDEN == plant)
    area = np.array([x, y]).T
    islands = find_islands(x, y, plant, GARDEN)
    for island in islands:
        area = np.array(island).size // 2
        perimiter, boundary_points = calculate_perimiter(island, plant)
        result_1 += area * perimiter
        print(f"{plant=}")
        corners = 0
        for p in boundary_points:
            # plot_garden(p, plant)
            c = count_point_corners(p, island, plant)
            print(f"This point has {c} corners")
            corners += c
            print(f"Total {corners=}")
            # input("----")
        result_2 += area * corners
        # m = f"{plant=}\n{corners=}"
        # message.append(m)


# for m in message:
#     print(m)
LOW = 512704
HIGH = 986593
# assert LOW < result_2 < HIGH, f"{result_2} not in range ({LOW}-{HIGH})"
print("1:", result_1)
print("2:", result_2)
