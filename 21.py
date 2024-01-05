import math
import queue


puzzle = [line for line in open("inputs/21.txt").read().strip().split("\n")]

# for l in puzzle:
#     print(l)

LIMIT = 26501365

HEIGHT = len(puzzle)
WIDTH = len(puzzle[0])


def find_start(puzzle):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if puzzle[y][x] == "S":
                return (y, x)


def get_neighbours(puzzle, y, x):
    for yd, xd in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        yn, xn = y + yd, x + xd
        if 0 <= yn < HEIGHT and 0 <= xn < WIDTH:  # and puzzle[yn][xn] != "#":
            yield (yn, xn)


def bfs(puzzle, start, limit):
    q = queue.Queue()
    distance_map = {start: 0}
    obstacle_map = {}

    q.put((start, 0))
    while not q.empty():
        current, distance = q.get()
        for neighbour in get_neighbours(puzzle, *current):
            if (
                neighbour not in distance_map
                and distance < limit
                and puzzle[neighbour[0]][neighbour[1]] != "#"
            ):
                distance_map[neighbour] = distance + 1
                q.put((neighbour, distance + 1))
            elif puzzle[neighbour[0]][neighbour[1]] == "#":
                obstacle_map[neighbour] = distance + 1

    return distance_map, obstacle_map


def get_points_in_one_graph(puzzle, start_point, even_steps):
    distance_map = bfs(puzzle, start_point, float("inf"))
    modulo_result = 0 if even_steps else 1
    result = 0
    for y in range(WIDTH):
        for x in range(HEIGHT):
            if (
                puzzle[y][x] != "#"
                and (y, x) in distance_map
                and distance_map[(y, x)] % 2 == modulo_result
            ):
                yield (y, x)


def count_points_in_map(distance_map, even):
    modulo = 0 if even else 1
    return len([v for v in distance_map.values() if v % 2 == modulo])


print(f"{WIDTH=}")
print(f"{HEIGHT=}")
limit = LIMIT
# limit = 3*WIDTH + LIMIT % WIDTH
start = find_start(puzzle)
distance_map, obstacle_map = bfs(puzzle, start, limit)
central_half_odd, _ = bfs(puzzle, start, limit % WIDTH)
central_half_even, _ = bfs(puzzle, start, limit % WIDTH + 1)
A1 = count_points_in_map(distance_map, even=False)
A0 = count_points_in_map(distance_map, even=True)
c0 = count_points_in_map(central_half_even, even=True)
c1 = count_points_in_map(central_half_odd, even=False)
print(f"{c0=}")
print(f"{c1=}")
print(f"{A0=}")
print(f"{A1=}")


def count_points(limit, width):
    n = math.ceil(limit / width)
    print(n)
    return (n * c1) - (2 * c0) + (n * (n - 1)) * (A1 + A0)


result = count_points(limit, WIDTH)

HIGH = 702322213546735
LOWW = 626938015685956
wrong = [627961538164641, 627961516113614, 627961538164121]
print(f"{result=}")
assert LOWW < result < HIGH, "not in range"
assert result not in wrong, "already tried"


#
def draw(puzzle, distance_map, even):
    modulo = 0 if even else 1
    result = ""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            p = (y, x)
            if p in distance_map and distance_map[p] % 2 == modulo:
                result += "O"
            else:
                result += puzzle[y][x]
        result += "\n"
    return result


even_drawing = draw(puzzle, distance_map, True).split("\n")
odd_drawing = draw(puzzle, distance_map, False).split("\n")

# for r1, r2 in zip(even_drawing, odd_drawing):
#     print(r1 + r2)


# start = find_start(puzzle)
# # limit = 3
# y, x = start
# points = [(y, x - limit), (y - limit, x), (y, x + limit), (y + limit, x)]
# # print(points)
# polygon = shapely.Polygon(points)
# print(polygon.area)
# # print(polygon.length / 4)
# i = polygon.area - limit * 2 + 1
# d = (2 * limit + 1) / 2**0.5
# o = outer / 4
# print(f"{o}")
# man = abs(y - y - limit) + abs(x - limit - x)
# print(man / 2 * 4)
