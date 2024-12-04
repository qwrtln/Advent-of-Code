import itertools

from pprint import pprint


from common import read_file


LOW_X = LOW_Y = 10**10
HIGH_X = HIGH_Y = 0
SOURCE = (500, 0)

FLOOR = HIGH_Y + 2


def find_edge_points(x0, x1, y0, y1):
    global LOW_X, LOW_Y, HIGH_X, HIGH_Y, FLOOR
    if x0 < LOW_X:
        LOW_X = x0
    if x1 < LOW_X:
        LOW_X = x1
    if y0 < LOW_Y:
        LOW_Y = y0
    if y1 < LOW_Y:
        LOW_Y = y1
    if x0 > HIGH_X:
        HIGH_X = x0
    if x1 > HIGH_X:
        HIGH_X = x1
    if y0 > HIGH_Y:
        HIGH_Y = y0
        FLOOR = HIGH_Y + 2
    if y1 > HIGH_Y:
        HIGH_Y = y1
        FLOOR = HIGH_Y + 2


def visualize_cave(rocks, sands):
    global LOW_X
    normalized_rocks = set()
    normalized_sands = set()
    for rock in rocks:
        x, y = rock
        normalized_rocks.add((x - LOW_X, y))
    for sand in sands:
        x, y = sand
        normalized_sands.add((x - LOW_X, y))

    cave = ""
    for i in range(FLOOR + 1):
        for j in range(HIGH_X - LOW_X + 7):
            if (j, i) in normalized_rocks:
                cave += "#"
            elif (j, i) in normalized_sands:
                cave += "o"
            elif (j + LOW_X, i) == SOURCE and (j + LOW_X, i) not in sands:
                cave += "+"
            else:
                cave += "."
        cave += "\n"

    print(cave)
    

def move_sand(x, y, rocks, sands):
    new_sands = [(x, y+1), (x-1, y+1), (x+1, y+1)]
    for sand in new_sands:
        if sand not in rocks and sand not in sands:
            return sand
    return (x, y)


def add_sand(sands, rocks):
    global HIGH_Y
    x, y = SOURCE[0], SOURCE[1]
    while True:
        new_position = move_sand(x, y, rocks, sands)
        if new_position == SOURCE:
            break
        if new_position == (x, y):
            return new_position
        x, y = new_position


def add_floor(rocks):
    for x in range(LOW_X - 500, HIGH_X + 500):
        rocks.add((x, HIGH_Y + 2))


def find_sandhill_edges():
    x, y = SOURCE
    edges = set()
    x1 = x2 = x
    while y != FLOOR:
        y += 1
        x1 += 1
        x2 -= 1
        edges.add((x1, y))
        edges.add((x2, y))
    return edges, int(0.5 * y * (x1 - x2))



if __name__ == "__main__":
    puzzle = read_file("14").split("\n")[:-1]

    potential_overhangs = set()
    actual_overhangs = set()

    rocks = set()
    for line in puzzle:
        points = line.split(" -> ")
        for i in range(1, len(points)):
            x0, y0 = [int(c) for c in points[i - 1].split(",")]
            x1, y1 = [int(c) for c in points[i].split(",")]
            find_edge_points(x0, x1, y0, y1)
            if x0 == x1:
                start, end = (y0, y1) if y0 < y1 else (y1, y0)
                for j in range(start, end + 1):
                    rocks.add((x0, j))
            else:
                start, end = (x0, x1) if x0 < x1 else (x1, x0)
                if end - start > 1:
                    potential_overhangs.add((start, end, y0))
                for j in range(start, end + 1):
                    rocks.add((j, y0))

    for po in potential_overhangs:
        x0, x1, y = po
        x = x0
        overhang_start = x0
        while x < x1:
            if (x, y + 1) in rocks and x - overhang_start >= 3:
                actual_overhangs.add((overhang_start, x, y))
                overhang_start = x + 1 
            x += 1
        if x1 - overhang_start >= 2:
            actual_overhangs.add((overhang_start, x1, y))

    edges, max_possible_size = find_sandhill_edges()
    size_without_rocks = max_possible_size - len(rocks)
    print(f"{max_possible_size=}")

    add_floor(rocks)
    overhang_spots = 0
    overhang_points = set()
    for ao in actual_overhangs:
        x0, x1, y = ao
        x_a = x0 + 1
        x_b = x1
        while x_a != x_b:
            for x in range(x_a, x_b):
                if (x, y + 1) not in rocks:
                    overhang_spots += 1
                    overhang_points.add((x, y+1))
            y += 1
            if y >= FLOOR:
                break
            x_a += 1
            x_b -= 1
    #print(f"{overhang_spots=}")
    #print(f"{len(overhang_points)=}")

    size_without_overhangs = size_without_rocks - overhang_spots
    print(f"{size_without_overhangs=}")

    sands = set() 
    LOW_X -= 155
    HIGH_X += 100
    for i in itertools.count():
        new_sand = add_sand(sands, rocks)
        if new_sand:
            sands.add(add_sand(sands, rocks))
        else:
            print(len(sands)+1)
            visualize_cave(rocks, sands)
            break
        if i % 100 == 0:
            pass
            #visualize_cave(rocks, sands)

        
