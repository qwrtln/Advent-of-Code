import collections
import itertools

puzzle = [line for line in open("inputs/08.txt").read().strip().split("\n")]

HEIGHT = len(puzzle)
WIDTH = len(puzzle[0])


ANTENNAS_MAPPING = collections.defaultdict(list)
LOCATION_MAPPING = {}

for y in range(len(puzzle)):
    for x in range(len(puzzle[y])):
        if puzzle[y][x] != ".":
            ANTENNAS_MAPPING[puzzle[y][x]].append((y, x))
            LOCATION_MAPPING[(y, x)] = puzzle[y][x]


def get_neighbouring_antinodes(p1, p2):
    if p1[0] < p2[0]:
        dy = p2[0] - p1[0]
        a_y_1 = p1[0] - dy
        a_y_2 = p2[0] + dy
    else:
        dy = p1[0] - p2[0]
        a_y_1 = p1[0] + dy
        a_y_2 = p2[0] - dy
    if p1[1] < p2[1]:
        dx = p2[1] - p1[1]
        a_x_1 = p1[1] - dx
        a_x_2 = p2[1] + dx
    else:
        dx = p1[1] - p2[1]
        a_x_1 = p1[1] + dx
        a_x_2 = p2[1] - dx
    return (a_y_1, a_x_1), (a_y_2, a_x_2)


def get_all_antinode_positions(p1, p2):
    a_y_1, a_y_2, a_x_1, a_x_2 = [], [], [], []
    if p1[0] < p2[0]:
        dy = p2[0] - p1[0]
        a_y_1 = list(range(p1[0], -1, -dy))
        a_y_2 = list(range(p2[0], HEIGHT, dy))
    else:
        dy = p1[0] - p2[0]
        a_y_1 = list(range(p1[0], HEIGHT, dy))
        a_y_2 = list(range(p2[0], -1, -dy))
    if p1[1] < p2[1]:
        dx = p2[1] - p1[1]
        a_x_1 = list(range(p1[1], -1, -dx))
        a_x_2 = list(range(p2[1], WIDTH, dx))
    else:
        dx = p1[1] - p2[1]
        a_x_1 = list(range(p1[1], WIDTH, dx))
        a_x_2 = list(range(p2[1], -1, -dx))
    for y, x in zip(a_y_1, a_x_1):
        yield (y, x)
    for y, x in zip(a_y_2, a_x_2):
        yield (y, x)
    yield p1
    return p2


def point_in_map(p):
    if p[0] in range(HEIGHT) and p[1] in range(WIDTH):
        return True
    return False


def count_antinodes(mapping, neighbouring_func):
    anti_positions = set()
    for node, positions in mapping.items():
        for p1, p2 in itertools.combinations(positions, 2):
            for node in neighbouring_func(p1, p2):
                if point_in_map(node):
                    anti_positions.add(node)
    return len(anti_positions)


print("1:", count_antinodes(ANTENNAS_MAPPING, get_neighbouring_antinodes))
print("2:", count_antinodes(ANTENNAS_MAPPING, get_all_antinode_positions))
