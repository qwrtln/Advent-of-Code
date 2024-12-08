import collections
import itertools

puzzle = [line for line in open("inputs/08.txt").read().strip().split("\n")]

HEIGHT = len(puzzle)
WIDTH = len(puzzle[0])


def parse_puzzle(puzzle):
    antennas_mapping = collections.defaultdict(list)
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            if puzzle[y][x] != ".":
                antennas_mapping[puzzle[y][x]].append((y, x))
    return antennas_mapping


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
    return [
        p
        for p in [(a_y_1, a_x_1), (a_y_2, a_x_2)]
        if p[0] in range(HEIGHT) and p[1] in range(WIDTH)
    ]


def get_all_antinodes(p1, p2):
    a_y_1, a_y_2, a_x_1, a_x_2 = [], [], [], []
    if p1[0] < p2[0]:
        dy = p2[0] - p1[0]
        a_y_1 = range(p1[0], -1, -dy)
        a_y_2 = range(p2[0], HEIGHT, dy)
    else:
        dy = p1[0] - p2[0]
        a_y_1 = range(p1[0], HEIGHT, dy)
        a_y_2 = range(p2[0], -1, -dy)
    if p1[1] < p2[1]:
        dx = p2[1] - p1[1]
        a_x_1 = range(p1[1], -1, -dx)
        a_x_2 = range(p2[1], WIDTH, dx)
    else:
        dx = p1[1] - p2[1]
        a_x_1 = range(p1[1], WIDTH, dx)
        a_x_2 = range(p2[1], -1, -dx)
    yield from zip(a_y_1, a_x_1)
    yield from zip(a_y_2, a_x_2)
    return (p1, p2)


def count_antinodes(mapping, neighbouring_func):
    anti_positions = set()
    for positions in mapping.values():
        for p1, p2 in itertools.combinations(positions, 2):
            anti_positions.update(neighbouring_func(p1, p2))
    return len(anti_positions)


antennas_mapping = parse_puzzle(puzzle)
print("1:", count_antinodes(antennas_mapping, get_neighbouring_antinodes))
print("2:", count_antinodes(antennas_mapping, get_all_antinodes))
